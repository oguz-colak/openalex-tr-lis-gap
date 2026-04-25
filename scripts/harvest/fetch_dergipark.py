"""
DergiPark + bd.org.tr — ListRecords tabanlı hızlı hasat
AGENTS.md Kural 1: oai_mods (DergiPark), oai_dc (bd.org.tr — mods desteklemiyor)
AGENTS.md Kural 2: Her yanıtta XML <error> kontrolü
AGENTS.md Kural 3: Pydantic uyumlu dict çıktısı
AGENTS.md Kural 4: completeListSize vs saved_count assertion
AGENTS.md Kural 5: Her sayfada state file yazılır
"""

import json
import logging
import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional

import requests

# ---------------------------------------------------------------------------
# Sabitler
# ---------------------------------------------------------------------------
DERGIPARK_URL = "https://dergipark.org.tr/api/public/oai/"
BD_URL        = "https://bd.org.tr/oai/"

JOURNALS = [
    {"name": "Türk Kütüphaneciliği",          "set": "tk",    "base_url": DERGIPARK_URL, "format": "oai_mods"},
    {"name": "Bilgi Yönetimi",                 "set": "by",    "base_url": DERGIPARK_URL, "format": "oai_mods"},
    {"name": "LAMRe",                          "set": "lamre", "base_url": DERGIPARK_URL, "format": "oai_mods"},
    {"name": "Arşiv Dünyası",                  "set": "ad",    "base_url": DERGIPARK_URL, "format": "oai_mods"},
    {"name": "Bilgi ve Belge Araştırmaları",   "set": "bel",   "base_url": DERGIPARK_URL, "format": "oai_mods"},
    {"name": "Bilgi Dünyası",                  "set": None,    "base_url": BD_URL,        "format": "oai_dc"},
]

ROOT         = Path(__file__).parent.parent
JOURNALS_DIR = ROOT / "data/raw/dergipark_journals"
STATE_FILE   = ROOT / "data/raw/dergipark_state.json"
OUTPUT       = ROOT / "data/raw/dergipark_records.jsonl"

OAI_NS  = "http://www.openarchives.org/OAI/2.0/"
MODS_NS = "http://www.loc.gov/mods/v3"
DC_NS   = "http://purl.org/dc/elements/1.1/"

MAX_RETRIES    = 3
BACKOFF_FACTOR = 2
PAGE_SLEEP     = 2.0  # sayfa arası bekleme (rate limiting için)

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Yardımcı: HTTP GET + OAI hata kontrolü (AGENTS.md Kural 2)
# ---------------------------------------------------------------------------
def oai_get(base_url: str, params: dict) -> ET.Element:
    ns = {"oai": OAI_NS}
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(base_url, params=params, timeout=30)
            if r.status_code == 429:
                wait = int(r.headers.get("Retry-After", 60))
                log.warning("HTTP 429 — %d saniye bekleniyor ...", wait)
                time.sleep(wait)
                raise ValueError("HTTP 429")
            if r.status_code != 200:
                raise ValueError(f"HTTP {r.status_code}")
            root = ET.fromstring(r.content)
            err = root.find(".//oai:error", ns)
            if err is not None:
                code = err.get("code", "?")
                msg  = err.text or ""
                if code == "noRecordsMatch":
                    return root
                raise ValueError(f"OAI-PMH error [{code}]: {msg}")
            return root
        except (requests.RequestException, ValueError, ET.ParseError) as exc:
            log.warning("Deneme %d/%d başarısız: %s", attempt, MAX_RETRIES, exc)
            if attempt < MAX_RETRIES:
                time.sleep(BACKOFF_FACTOR ** attempt)
    raise RuntimeError(f"Maksimum deneme aşıldı: {params}")

# ---------------------------------------------------------------------------
# Parse — oai_mods  (record_el = <oai:record> elementi)
# ---------------------------------------------------------------------------
def _text(el, path, ns):
    found = el.find(path, ns)
    return (found.text or "").strip() if found is not None else None

def parse_mods(record_el: ET.Element, source_name: str) -> Optional[dict]:
    ns_mods = {"mods": MODS_NS}
    mods = record_el.find(".//mods:mods", ns_mods)
    if mods is None:
        return None

    titles = {}
    for ti in mods.findall("mods:titleInfo", ns_mods):
        lang = ti.get("{http://www.w3.org/XML/1998/namespace}lang", "?")
        t    = ti.find("mods:title", ns_mods)
        if t is not None and t.text:
            titles[lang] = t.text.strip()

    authors = []
    for n in mods.findall("mods:name[@type='personal']", ns_mods):
        given  = n.findtext("mods:namePart[@type='given']",  namespaces=ns_mods) or ""
        family = n.findtext("mods:namePart[@type='family']", namespaces=ns_mods) or ""
        full   = f"{given} {family}".strip()
        if full:
            authors.append(full)

    abstracts = {}
    for ab in mods.findall("mods:abstract", ns_mods):
        lang = ab.get("{http://www.w3.org/XML/1998/namespace}lang", "?")
        if ab.text:
            abstracts[lang] = ab.text.strip()

    doi = next(
        (el.text for el in mods.findall("mods:identifier", ns_mods) if el.get("type") == "doi"),
        None,
    )
    if doi and doi.startswith("https://doi.org/"):
        doi = doi[len("https://doi.org/"):]

    date_issued = _text(mods, "mods:originInfo/mods:dateIssued", ns_mods)
    year_match  = re.search(r"\b(1[89]\d{2}|20[012]\d)\b", date_issued or "")

    return {
        "source_journal":   source_name,
        "metadata_format":  "oai_mods",
        "title_tr":         titles.get("tr-TR") or titles.get("tr"),
        "title_en":         titles.get("en-US") or titles.get("en"),
        "language":         _text(mods, "mods:language/mods:languageTerm", ns_mods),
        "publication_year": int(year_match.group(1)) if year_match else None,
        "date_issued":      date_issued,
        "identifier_doi":   doi,
        "authors":          authors,
        "abstract_tr":      abstracts.get("tr-TR") or abstracts.get("tr"),
        "abstract_en":      abstracts.get("en-US") or abstracts.get("en"),
        "publisher":        _text(mods, "mods:originInfo/mods:publisher", ns_mods),
        "funders":          [],
        "ror_ids":          [],
    }

# ---------------------------------------------------------------------------
# Parse — oai_dc  (Bilgi Dünyası — bd.org.tr oai_mods desteklemiyor)
# ---------------------------------------------------------------------------
def parse_dc(record_el: ET.Element, source_name: str) -> Optional[dict]:
    ns_dc = {"dc": DC_NS}
    dc = record_el.find(".//{http://www.openarchives.org/OAI/2.0/oai_dc/}dc")
    if dc is None:
        return None

    def all_text(tag):
        return [el.text.strip() for el in dc.findall(f"dc:{tag}", ns_dc) if el.text]

    titles       = all_text("title")
    creators     = all_text("creator")
    dates        = all_text("date")
    languages    = all_text("language")
    identifiers  = all_text("identifier")
    descriptions = all_text("description")

    doi = next((i for i in identifiers if i.startswith("10.")), None)
    if not doi:
        doi_full = next((i for i in identifiers if "doi.org" in i), None)
        if doi_full:
            doi = re.sub(r".*doi\.org/", "", doi_full)

    date_str   = dates[0] if dates else None
    year_match = re.search(r"\b(1[89]\d{2}|20[012]\d)\b", date_str or "")

    return {
        "source_journal":   source_name,
        "metadata_format":  "oai_dc",
        "title_tr":         titles[0] if titles else None,
        "title_en":         titles[1] if len(titles) > 1 else None,
        "language":         languages[0] if languages else None,
        "publication_year": int(year_match.group(1)) if year_match else None,
        "date_issued":      date_str,
        "identifier_doi":   doi,
        "authors":          creators,
        "abstract_tr":      descriptions[0] if descriptions else None,
        "abstract_en":      descriptions[1] if len(descriptions) > 1 else None,
        "publisher":        None,
        "funders":          [],
        "ror_ids":          [],
    }

# ---------------------------------------------------------------------------
# State file yardımcıları (AGENTS.md Kural 5)
# ---------------------------------------------------------------------------
def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}

def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

# ---------------------------------------------------------------------------
# ListRecords döngüsü — tek dergi
# ---------------------------------------------------------------------------
def harvest_journal(journal: dict, state: dict) -> int:
    name   = journal["name"]
    base   = journal["base_url"]
    fmt    = journal["format"]
    set_   = journal.get("set")
    parser = parse_mods if fmt == "oai_mods" else parse_dc

    j_state = state.setdefault(name, {"complete": False, "saved_count": 0})

    if j_state.get("complete"):
        log.info("[%s] Zaten tamamlandı (%d kayıt), atlanıyor.", name, j_state["saved_count"])
        return j_state["saved_count"]

    out_file = JOURNALS_DIR / f"{set_ or 'bd'}.jsonl"
    log.info("[%s] ListRecords başlıyor ...", name)

    ns_oai            = {"oai": OAI_NS}
    params            = {"verb": "ListRecords", "metadataPrefix": fmt}
    if set_:
        params["set"] = set_

    saved              = 0
    complete_list_size = None
    page               = 0

    with open(out_file, "w", encoding="utf-8") as fh:
        while True:
            root     = oai_get(base, params)
            token_el = root.find(".//oai:resumptionToken", ns_oai)

            # completeListSize — ilk sayfada okunur (AGENTS.md Kural 4)
            if complete_list_size is None and token_el is not None:
                cls = token_el.get("completeListSize")
                if cls:
                    complete_list_size = int(cls)
                    log.info("[%s] completeListSize = %d", name, complete_list_size)

            for rec in root.findall(".//oai:record", ns_oai):
                parsed = parser(rec, name)
                if parsed:
                    fh.write(json.dumps(parsed, ensure_ascii=False) + "\n")
                    saved += 1

            page += 1
            log.info("[%s] Sayfa %d tamamlandı — toplam %d kayıt", name, page, saved)

            # AGENTS.md Kural 5: Her sayfada state kaydet
            j_state["saved_count"] = saved
            save_state(state)

            if token_el is None or not (token_el.text or "").strip():
                break
            params = {"verb": "ListRecords", "resumptionToken": token_el.text.strip()}
            time.sleep(PAGE_SLEEP)

    j_state["complete"]          = True
    j_state["saved_count"]       = saved
    j_state["complete_list_size"] = complete_list_size
    save_state(state)

    # AGENTS.md Kural 4: completeListSize doğrulaması
    if complete_list_size is not None:
        missing = complete_list_size - saved
        if missing:
            log.warning("[%s] ⚠ %d kayıt eksik (completeListSize=%d, saved=%d)",
                        name, missing, complete_list_size, saved)
        else:
            log.info("[%s] ✓ Doğrulama başarılı: %d/%d", name, saved, complete_list_size)
        assert saved <= complete_list_size, (
            f"[{name}] Count mismatch: saved={saved} > completeListSize={complete_list_size}"
        )
    else:
        log.info("[%s] ✓ completeListSize bilinmiyor — %d kayıt kaydedildi", name, saved)

    return saved

# ---------------------------------------------------------------------------
# Tüm dergi dosyalarını tek OUTPUT'ta birleştir
# ---------------------------------------------------------------------------
def combine_outputs() -> int:
    total = 0
    with open(OUTPUT, "w", encoding="utf-8") as out:
        for f in sorted(JOURNALS_DIR.glob("*.jsonl")):
            for line in f.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    out.write(line + "\n")
                    total += 1
    log.info("Birleştirme tamamlandı: %d kayıt → %s", total, OUTPUT)
    return total

# ---------------------------------------------------------------------------
# Ana döngü
# ---------------------------------------------------------------------------
def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(ROOT / "data/raw/dergipark_fetch.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    JOURNALS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    state   = load_state()
    results = {}

    for journal in JOURNALS:
        name = journal["name"]
        log.info("=" * 60)
        log.info("Dergi: %s", name)
        results[name] = harvest_journal(journal, state)

    log.info("=" * 60)
    log.info("ÖZET")
    for name, saved in results.items():
        log.info("  %-40s %4d kayıt", name, saved)

    total = combine_outputs()
    log.info("TOPLAM: %d kayıt → %s", total, OUTPUT)

if __name__ == "__main__":
    main()
