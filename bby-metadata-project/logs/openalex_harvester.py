"""OpenAlex API'sinden BBY dergilerine ait tüm üstverileri toplar."""

import json
import logging
import os
import time
from pathlib import Path

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("openalex_harvest.log", encoding="utf-8")],
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "02_data_collection" / "raw_data" / "openalex"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://api.openalex.org/works"
SOURCES_URL = "https://api.openalex.org/sources"
EMAIL = os.getenv("OPENALEX_MAILTO")

JOURNALS = {
    "turk_kutuphaneciligi": {
        "issn": ["2147-9682"],
        "label": "Türk Kütüphaneciliği",
        "source_id": None,
    },
    "bilgi_dunyasi": {
        "issn": ["2148-354X"],
        "label": "Bilgi Dünyası",
        "source_id": None,
    },
    "bilgi_belge_arastirmalari": {
        "issn": ["2148-8975"],
        "label": "Bilgi ve Belge Araştırmaları",
        "source_id": None,
    },
    "lam_research_journal": {
        "issn": ["2718-0832"],
        "label": "Library, Archive and Museum Research Journal",
        "source_id": None,
    },
    "arsiv_dunyasi": {
        "issn": ["2147-2599", "2717-7335"],
        "label": "Arşiv Dünyası",
        "source_id": None,
    },
    "bilgi_yonetimi": {
        "issn": ["2636-8544"],
        "label": "Bilgi Yönetimi",
        "source_id": None,
    },
}


def resolve_source_id(issn_list: list[str], label: str) -> str | None:
    """ISSN listesinden OpenAlex Source ID'yi çözer."""
    for issn in issn_list:
        try:
            params = {"filter": f"issn:{issn}"}
            if EMAIL:
                params["mailto"] = EMAIL
            resp = requests.get(SOURCES_URL, params=params, timeout=15)
            resp.raise_for_status()
            results = resp.json().get("results", [])
            if results:
                src_id = results[0]["id"].split("/")[-1]  # "S2736521800"
                logger.info(f"[{label}] Source ID çözüldü: {src_id}")
                return src_id
        except requests.RequestException as e:
            logger.warning(f"[{label}] Source ID sorgusu başarısız ({issn}): {e}")
    logger.warning(f"[{label}] Source ID bulunamadı, ISSN filtresi kullanılacak.")
    return None


def is_valid_record(work: dict, issn_list: list[str], source_id: str | None) -> bool:
    """Kaydın hedef dergiye ait olduğunu doğrular.

    Öncelik sırası:
    1. primary_location.source.id eşleşmesi (en kesin)
    2. primary_location.source.issn eşleşmesi
    3. primary_location.source.issn DOLU ve eşleşmiyorsa → kesinlikle başka dergi, reddet
       (ISSN dergi-özgüdür; source_id platform/repo olabilir, yanlış source_id tek başına geçersiz kılmaz)
    4. primary_location.source.issn BOŞSA → fallback: herhangi bir location içinde source.id eşleşmesi
       (DergiPark/platform primary'li veya indekslenmemiş eski kayıtları kapsar)
    """
    pl = work.get("primary_location") or {}
    src = pl.get("source") or {}

    if source_id and src.get("id", "").endswith(source_id):
        return True

    work_issns = src.get("issn") or []
    if any(issn in work_issns for issn in issn_list):
        return True

    if work_issns:
        return False

    if source_id:
        for loc in (work.get("locations") or []):
            ls = loc.get("source") or {}
            if (ls.get("id") or "").endswith(source_id):
                return True

    return False


def fetch_works_by_issn(
    issn_list: list[str], label: str, source_id: str | None = None
) -> list[dict]:
    """Verilen Source ID veya ISSN listesi için OpenAlex'ten tüm eserleri çeker.

    Source ID varsa locations.source.id: filtresi kullanılır; bu sayede derginin
    primary_location yerine DOAJ/DergiPark gibi repository'lerde listelendiği
    eski kayıtlar da sorgu kapsamına girer. Post-fetch is_valid_record doğrulaması
    olası kirli kayıtları eler.
    """
    if source_id:
        issn_filter = f"locations.source.id:{source_id}"
    else:
        issn_filter = "primary_location.source.issn:" + "|".join(issn_list)

    params = {
        "filter": issn_filter,
        "per-page": 200,
        "cursor": "*",
    }
    if EMAIL:
        params["mailto"] = EMAIL

    all_works: list[dict] = []
    page = 1

    while True:
        try:
            logger.info(f"[{label}] Sayfa {page} çekiliyor...")
            response = requests.get(BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            logger.error(f"[{label}] Sayfa {page} isteği başarısız: {e}")
            break

        results = data.get("results", [])

        valid = [w for w in results if is_valid_record(w, issn_list, source_id)]
        rejected = len(results) - len(valid)
        if rejected:
            logger.warning(f"[{label}] {rejected} kayıt doğrulama dışı bırakıldı.")

        all_works.extend(valid)
        logger.info(f"[{label}] {len(valid)} kayıt alındı (toplam: {len(all_works)})")

        next_cursor = data.get("meta", {}).get("next_cursor")
        if not next_cursor:
            break

        params["cursor"] = next_cursor
        page += 1
        time.sleep(0.5)

    return all_works


def exponential_backoff(func, *args, max_retries: int = 5, **kwargs):
    """Başarısız istekleri üstel geri çekilme ile yeniden dener."""
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 429:
                wait = 2 ** attempt
                logger.warning(f"Rate limit aşıldı. {wait}s bekleniyor...")
                time.sleep(wait)
            else:
                raise
    logger.error("Maksimum yeniden deneme sayısına ulaşıldı.")
    return []


def filter_existing_json(journal_key: str, issn_list: list[str], source_id: str | None) -> None:
    """Mevcut JSON dosyasından geçersiz kayıtları kaldırır (yeniden harvest gerektirmez)."""
    out_file = OUTPUT_DIR / f"{journal_key}.json"
    if not out_file.exists():
        logger.warning(f"{out_file} bulunamadı, atlanıyor.")
        return
    with open(out_file, encoding="utf-8") as f:
        works = json.load(f)
    before = len(works)
    valid = [w for w in works if is_valid_record(w, issn_list, source_id)]
    after = len(valid)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(valid, f, ensure_ascii=False, indent=2)
    logger.info(f"[{journal_key}] Filtre: {before} → {after} kayıt ({before - after} kaldırıldı)")


def save_works(works: list[dict], journal_key: str) -> Path:
    """Eserleri JSON dosyasına kaydeder ve dosya yolunu döndürür."""
    out_file = OUTPUT_DIR / f"{journal_key}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(works, f, ensure_ascii=False, indent=2)
    logger.info(f"Kaydedildi: {out_file} ({len(works)} kayıt)")
    return out_file


def harvest_all() -> dict:
    """Tüm dergiler için veri toplar ve özet istatistikleri döndürür."""
    summary: dict = {}

    for key, meta in JOURNALS.items():
        logger.info(f"=== {meta['label']} başlıyor ===")

        src_id = resolve_source_id(meta["issn"], meta["label"])
        time.sleep(0.5)

        works = exponential_backoff(
            fetch_works_by_issn, meta["issn"], meta["label"], source_id=src_id
        )
        out_file = save_works(works, key)
        summary[key] = {
            "label": meta["label"],
            "issn": meta["issn"],
            "source_id": src_id,
            "record_count": len(works),
            "output_file": str(out_file),
        }
        time.sleep(1)

    log_file = OUTPUT_DIR.parent / "harvest_log.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(
            {"source": "openalex", "harvested_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"), "journals": summary},
            f,
            ensure_ascii=False,
            indent=2,
        )
    logger.info(f"Özet log kaydedildi: {log_file}")
    return summary


if __name__ == "__main__":
    # Mevcut bilgi_dunyasi.json'u temizle (yeniden harvest gerekmez)
    _src_id = resolve_source_id(JOURNALS["bilgi_dunyasi"]["issn"], "Bilgi Dünyası")
    filter_existing_json("bilgi_dunyasi", JOURNALS["bilgi_dunyasi"]["issn"], _src_id)

    # Tam harvest için: harvest_all() satırını aktif et
    # result = harvest_all()
    # total = sum(v["record_count"] for v in result.values())
    # logger.info(f"Toplama tamamlandı. Toplam kayıt: {total}")
