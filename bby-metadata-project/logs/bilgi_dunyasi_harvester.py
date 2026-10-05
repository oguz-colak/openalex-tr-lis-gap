"""Bilgi Dünyası dergisine ait üstverileri bd.org.tr OAI-PMH (MODS) ve TR-Dizin API'sinden toplar."""

import json
import logging
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bilgi_dunyasi_harvest.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_DIR = PROJECT_ROOT / "02_data_collection" / "raw_data" / "bilgi_dunyasi"
BASE_DIR.mkdir(parents=True, exist_ok=True)

OAI_OUT = BASE_DIR / "oai_bd.xml"
TRDIZIN_OUT = BASE_DIR / "trdizin.json"
HARVEST_LOG = Path(__file__).parent / "raw_data" / "harvest_log.json"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
OAI_ENDPOINT = "https://bd.org.tr/tr/oai"

# TR-Dizin: iki adımlı veri toplama:
#   1) /api/journalPublicationsById/<journal_id> dergideki yayınların ID listesini döndürür.
#      Bu endpoint sayfalama gerektirmez ancak her kayıt için yalnızca minimum `fields`
#      alanı (id, issue.year, publicationType) içerir; `_source` boştur.
#   2) /api/publicationById/<publication_id> her yayının tam `_source` üst verisini döndürür
#      (abstracts, authors+ORCID, doi, journal, references, subjects vb.).
TRDIZIN_LIST_ENDPOINT = "https://search.trdizin.gov.tr/api/journalPublicationsById/1227"
TRDIZIN_DETAIL_ENDPOINT = "https://search.trdizin.gov.tr/api/publicationById/{id}"
BILGI_DUNYASI_ISSN = "2148-354X"
BILGI_DUNYASI_JOURNAL_ID = "1227"

# TR-Dizin API requires the Origin header; without it all queries return 0 results.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; BBY-MetaResearch/1.0)",
    "Origin": "https://search.trdizin.gov.tr",
    "Referer": "https://search.trdizin.gov.tr/",
}

OAI_NS = {
    "oai": "http://www.openarchives.org/OAI/2.0/",
    "marc": "http://www.loc.gov/MARC21/slim",
}


# ===========================================================================
# Source 1 — OAI-PMH (bd.org.tr)
# ===========================================================================


def build_oai_params(resumption_token: str | None = None) -> dict:
    """İlk istek veya devam isteği için OAI-PMH parametre sözlüğü döndürür."""
    if resumption_token:
        return {"verb": "ListRecords", "resumptionToken": resumption_token}
    return {"verb": "ListRecords", "metadataPrefix": "marcxml"}


def fetch_oai_page(params: dict, max_retries: int = 5) -> ET.Element | None:
    """Tek bir OAI-PMH sayfasını çeker; 503 hatalarında exponential backoff uygular."""
    for attempt in range(max_retries):
        try:
            response = requests.get(
                OAI_ENDPOINT, params=params, headers=HEADERS, timeout=30
            )
            response.raise_for_status()
            return ET.fromstring(response.content)
        except requests.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else None
            if status == 503 and attempt < max_retries - 1:
                wait = 5 * (2 ** attempt)  # 5, 10, 20, 40 s
                logger.warning(
                    f"503 alındı, {wait}s beklenip tekrar denenecek "
                    f"(deneme {attempt + 1}/{max_retries})..."
                )
                time.sleep(wait)
                continue
            logger.error(f"OAI HTTP hatası: {exc}")
            return None
        except requests.RequestException as exc:
            logger.error(f"OAI istek hatası: {exc}")
            return None
        except ET.ParseError as exc:
            logger.error(f"OAI XML ayrıştırma hatası: {exc}")
            return None
    return None


def extract_oai_records(root: ET.Element) -> list[ET.Element]:
    """XML kök elementinden <record> elementlerini çıkarır."""
    return root.findall(".//oai:record", OAI_NS)


def extract_resumption_token(root: ET.Element) -> str | None:
    """Devam tokeni mevcut ve doluysa döndürür, değilse None."""
    token_el = root.find(".//oai:resumptionToken", OAI_NS)
    if token_el is not None and token_el.text and token_el.text.strip():
        return token_el.text.strip()
    return None


def check_oai_error(root: ET.Element) -> str | None:
    """OAI-PMH hata elementini kontrol eder; varsa hata kodunu döndürür."""
    err_el = root.find(".//oai:error", OAI_NS)
    if err_el is not None:
        return err_el.get("code", "unknown")
    return None


def harvest_oai() -> int:
    """bd.org.tr OAI-PMH endpoint'inden MODS formatında tüm kayıtları toplar ve XML dosyasına kaydeder."""
    collection = ET.Element(
        "OAI-PMH-Collection",
        journal="Bilgi Dünyası",
        source="bd.org.tr",
    )
    total = 0
    page = 1
    resumption_token: str | None = None

    while True:
        params = build_oai_params(resumption_token)
        logger.info(f"[OAI] Sayfa {page} çekiliyor...")

        xml_root = fetch_oai_page(params)
        if xml_root is None:
            logger.error(f"[OAI] Sayfa {page} alınamadı, döngü sonlandırılıyor.")
            break

        oai_error = check_oai_error(xml_root)
        if oai_error:
            logger.warning(f"[OAI] OAI-PMH hatası kodu: {oai_error}")
            collection.set("oai_error", oai_error)
            break

        records = extract_oai_records(xml_root)
        for rec in records:
            collection.append(rec)
        total += len(records)
        logger.info(f"[OAI] {len(records)} kayıt alındı (toplam: {total})")

        resumption_token = extract_resumption_token(xml_root)
        if not resumption_token:
            logger.info("[OAI] ResumptionToken bulunamadı — tüm sayfalar tamamlandı.")
            break

        page += 1
        time.sleep(1)

    tree = ET.ElementTree(collection)
    ET.indent(tree, space="  ")
    tree.write(OAI_OUT, encoding="utf-8", xml_declaration=True)
    logger.info(f"[OAI] {total} kayıt kaydedildi → {OAI_OUT}")
    return total


# ===========================================================================
# Source 2 — TR-Dizin API
# ===========================================================================


def fetch_trdizin_id_list() -> list[str]:
    """journalPublicationsById endpoint'inden Bilgi Dünyası yayın ID listesini çeker."""
    try:
        response = requests.get(TRDIZIN_LIST_ENDPOINT, headers=HEADERS, timeout=60)
        response.raise_for_status()
        data = response.json()
        hits = data.get("hits", {}).get("hits", [])
        return [hit.get("_id") for hit in hits if hit.get("_id")]
    except requests.RequestException as exc:
        logger.error(f"[TR-Dizin] ID listesi çekilemedi: {exc}")
        return []
    except (json.JSONDecodeError, AttributeError, TypeError) as exc:
        logger.error(f"[TR-Dizin] ID listesi JSON ayrıştırma hatası: {exc}")
        return []


def fetch_trdizin_detail(pub_id: str, max_retries: int = 3) -> dict | None:
    """publicationById endpoint'inden tek bir yayının tam `_source` verisini çeker."""
    url = TRDIZIN_DETAIL_ENDPOINT.format(id=pub_id)
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            data = response.json()
            hits = data.get("hits", {}).get("hits", [])
            if not hits:
                logger.warning(f"[TR-Dizin] {pub_id} için kayıt bulunamadı.")
                return None
            record = hits[0].get("_source", {}) or {}
            record["_trdizin_id"] = hits[0].get("_id", pub_id)
            record["_trdizin_address"] = data.get("trdizinAddress")
            return record
        except requests.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else None
            if status in (429, 503) and attempt < max_retries - 1:
                wait = 2 ** attempt * 2
                logger.warning(
                    f"[TR-Dizin] {pub_id} için {status}, {wait}s sonra tekrar denenecek..."
                )
                time.sleep(wait)
                continue
            logger.error(f"[TR-Dizin] {pub_id} HTTP hatası: {exc}")
            return None
        except requests.RequestException as exc:
            logger.error(f"[TR-Dizin] {pub_id} istek hatası: {exc}")
            return None
        except (json.JSONDecodeError, AttributeError, TypeError) as exc:
            logger.error(f"[TR-Dizin] {pub_id} JSON ayrıştırma hatası: {exc}")
            return None
    return None


def harvest_trdizin() -> int:
    """TR-Dizin'den Bilgi Dünyası yayınlarının tam üstverisini iki adımda toplar."""
    logger.info(
        f"[TR-Dizin] ID listesi çekiliyor (journal ID: {BILGI_DUNYASI_JOURNAL_ID})..."
    )
    id_list = fetch_trdizin_id_list()
    logger.info(f"[TR-Dizin] {len(id_list)} yayın ID alındı. Detaylar çekiliyor...")

    records: list[dict] = []
    for idx, pub_id in enumerate(id_list, 1):
        record = fetch_trdizin_detail(pub_id)
        if record is not None:
            records.append(record)
        if idx % 50 == 0:
            logger.info(f"[TR-Dizin] İlerleme: {idx}/{len(id_list)} (başarılı: {len(records)})")
        time.sleep(0.3)  # Nazik rate limiting

    with open(TRDIZIN_OUT, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    logger.info(
        f"[TR-Dizin] {len(records)}/{len(id_list)} kayıt kaydedildi → {TRDIZIN_OUT}"
    )
    return len(records)


# ===========================================================================
# Harvest log update
# ===========================================================================


def update_harvest_log(oai_count: int, trdizin_count: int) -> None:
    """harvest_log.json dosyasını bilgi_dunyasi bölümüyle günceller."""
    existing: dict = {}
    if HARVEST_LOG.exists():
        try:
            with open(HARVEST_LOG, encoding="utf-8") as f:
                existing = json.load(f)
        except (json.JSONDecodeError, OSError) as exc:
            logger.error(f"harvest_log.json okunamadı: {exc}")

    existing["bilgi_dunyasi"] = {
        "source_oai": "bd.org.tr",
        "source_trdizin": "trdizin",
        "harvested_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "oai_record_count": oai_count,
        "trdizin_record_count": trdizin_count,
    }

    try:
        with open(HARVEST_LOG, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
        logger.info(f"harvest_log.json güncellendi → {HARVEST_LOG}")
    except OSError as exc:
        logger.error(f"harvest_log.json yazılamadı: {exc}")


# ===========================================================================
# Entry point
# ===========================================================================


def main() -> None:
    """OAI-PMH ve TR-Dizin kaynaklarından Bilgi Dünyası üstverilerini toplar."""
    logger.info("=== Bilgi Dünyası Harvester başlıyor ===")

    logger.info("--- Kaynak 1: bd.org.tr OAI-PMH ---")
    oai_count = harvest_oai()

    logger.info("--- Kaynak 2: TR-Dizin API ---")
    trdizin_count = harvest_trdizin()

    logger.info("--- Harvest log güncelleniyor ---")
    update_harvest_log(oai_count, trdizin_count)

    logger.info(
        f"=== Tamamlandı. OAI: {oai_count} kayıt | TR-Dizin: {trdizin_count} kayıt ==="
    )


if __name__ == "__main__":
    main()
