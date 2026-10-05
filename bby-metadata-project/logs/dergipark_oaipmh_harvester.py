"""DergiPark OAI-PMH endpoint'inden BBY dergilerine ait MODS üstverilerini toplar."""

import logging
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("dergipark_harvest.log", encoding="utf-8")],
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "02_data_collection" / "raw_data" / "dergipark"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OAI_BASE = "https://dergipark.org.tr/api/public/oai/"
NS = {
    "oai": "http://www.openarchives.org/OAI/2.0/",
    "mods": "http://www.loc.gov/mods/v3",
    "oai_mods": "http://www.openarchives.org/OAI/2.0/oai_mods/",
}

JOURNALS = {
    "tk": "Türk Kütüphaneciliği",
    "bel": "Bilgi ve Belge Araştırmaları",
    "lamre": "Library, Archive and Museum Research Journal",
    "ad": "Arşiv Dünyası",
    "by": "Bilgi Yönetimi",
}


def build_params(set_code: str, resumption_token: str | None = None) -> dict:
    """İlk istek veya devam isteği için OAI-PMH parametrelerini oluşturur."""
    if resumption_token:
        return {"verb": "ListRecords", "resumptionToken": resumption_token}
    return {
        "verb": "ListRecords",
        "metadataPrefix": "oai_mods",
        "set": set_code,
    }


def fetch_page(params: dict, max_retries: int = 5) -> ET.Element | None:
    """Tek bir OAI-PMH sayfasını çeker; 503 hatalarında exponential backoff ile tekrar dener."""
    for attempt in range(max_retries):
        try:
            response = requests.get(OAI_BASE, params=params, timeout=30)
            response.raise_for_status()
            return ET.fromstring(response.content)
        except requests.HTTPError as e:
            err_response = e.response if e.response is not None else None
            status = err_response.status_code if err_response is not None else None
            if status == 503 and attempt < max_retries - 1:
                wait = 2 ** attempt * 5  # 5, 10, 20, 40 saniye
                logger.warning(f"503 alındı, {wait}s beklenip tekrar denenecek (deneme {attempt + 1}/{max_retries})...")
                time.sleep(wait)
                continue
            logger.error(f"İstek başarısız: {e}")
            return None
        except requests.RequestException as e:
            logger.error(f"İstek başarısız: {e}")
            return None
        except ET.ParseError as e:
            logger.error(f"XML ayrıştırma hatası: {e}")
            return None
    return None


def extract_records(root: ET.Element) -> list[ET.Element]:
    """XML kökünden kayıt elementlerini çıkarır."""
    return root.findall(".//oai:record", NS)


def extract_resumption_token(root: ET.Element) -> str | None:
    """Devam tokeni varsa döndürür, yoksa None."""
    token_el = root.find(".//oai:resumptionToken", NS)
    if token_el is not None and token_el.text and token_el.text.strip():
        return token_el.text.strip()
    return None


def check_oai_error(root: ET.Element) -> str | None:
    """OAI-PMH hata elementini kontrol eder; varsa hata kodunu döndürür."""
    error_el = root.find(".//oai:error", NS)
    if error_el is not None:
        return error_el.get("code", "unknown")
    return None


def harvest_journal(set_code: str, label: str) -> ET.Element:
    """Bir derginin tüm kayıtlarını OAI-PMH ile toplar ve birleşik XML döndürür."""
    root_el = ET.Element("OAI-PMH-Collection", journal=label, set=set_code)
    total = 0
    page = 1
    resumption_token: str | None = None

    while True:
        params = build_params(set_code, resumption_token)
        logger.info(f"[{label}] Sayfa {page} çekiliyor...")

        xml_root = fetch_page(params)
        if xml_root is None:
            logger.error(f"[{label}] Sayfa {page} alınamadı, atlanıyor.")
            break

        oai_error = check_oai_error(xml_root)
        if oai_error:
            logger.warning(f"[{label}] OAI-PMH hatası: {oai_error} — set kodu '{set_code}' geçersiz olabilir.")
            root_el.set("oai_error", oai_error)
            break

        records = extract_records(xml_root)
        for rec in records:
            root_el.append(rec)
        total += len(records)
        logger.info(f"[{label}] {len(records)} kayıt alındı (toplam: {total})")

        resumption_token = extract_resumption_token(xml_root)
        if not resumption_token:
            break

        page += 1
        time.sleep(1)

    return root_el


def save_xml(element: ET.Element, set_code: str) -> Path:
    """XML elementini dosyaya kaydeder ve yolu döndürür."""
    out_file = OUTPUT_DIR / f"{set_code}.xml"
    tree = ET.ElementTree(element)
    ET.indent(tree, space="  ")
    tree.write(out_file, encoding="utf-8", xml_declaration=True)
    logger.info(f"Kaydedildi: {out_file}")
    return out_file


def harvest_all() -> dict:
    """Tüm dergiler için OAI-PMH MODS veri toplama işlemini çalıştırır."""
    import json

    summary: dict = {}

    for code, label in JOURNALS.items():
        logger.info(f"=== {label} başlıyor ===")
        collection = harvest_journal(code, label)
        record_count = len(collection.findall("{http://www.openarchives.org/OAI/2.0/}record"))
        out_file = save_xml(collection, code)
        summary[code] = {
            "label": label,
            "record_count": record_count,
            "output_file": str(out_file),
        }
        time.sleep(2)

    log_file = OUTPUT_DIR.parent / "harvest_log.json"
    existing = {}
    if log_file.exists():
        with open(log_file, encoding="utf-8") as f:
            existing = json.load(f)

    existing["dergipark"] = {
        "source": "dergipark_oaipmh",
        "harvested_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "journals": summary,
    }

    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    logger.info(f"Özet log güncellendi: {log_file}")
    return summary


if __name__ == "__main__":
    result = harvest_all()
    total = sum(v["record_count"] for v in result.values())
    logger.info(f"Toplama tamamlandı. Toplam kayıt: {total}")
