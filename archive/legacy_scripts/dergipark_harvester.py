import re
import requests
import time
import os
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional

from models import ArticleMetadata
from fetch_dergipark import OAI_NS, MODS_NS

# Constants
BASE_URL = "https://dergipark.org.tr/api/public/oai/"
IDENTIFIER = "oai:dergipark.org.tr:article/1674520"
METADATA_PREFIXES = ["oai_mods"]  # AGENTS.md Kural 1: yalnızca oai_mods
MAX_RETRIES = 3
BACKOFF_FACTOR = 2

def fetch_metadata(metadata_prefix: str, identifier: str) -> Optional[str]:
    """
    Fetches XML metadata from DergiPark OAI-PMH with exponential backoff.
    """
    params = {
        "verb": "GetRecord",
        "metadataPrefix": metadata_prefix,
        "identifier": identifier
    }
    
    retries = 0
    while retries < MAX_RETRIES:
        try:
            print(f"[*] Fetching {metadata_prefix} for {identifier} (Attempt {retries + 1})...")
            response = requests.get(BASE_URL, params=params, timeout=30)
            
            if response.status_code == 200:
                return response.text
            else:
                print(f"[!] HTTP {response.status_code} received.")
                
        except requests.exceptions.RequestException as e:
            print(f"[!] Connection error: {e}")
            
        retries += 1
        if retries < MAX_RETRIES:
            wait_time = BACKOFF_FACTOR ** retries
            print(f"[*] Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
            
    return None

def check_oai_errors(xml_content: str) -> Optional[str]:
    """
    Checks if the OAI-PMH response contains an <error> element.
    Returns the error message if found, otherwise None.
    """
    try:
        root = ET.fromstring(xml_content)
        # OAI-PMH namespace is usually http://www.openarchives.org/OAI/2.0/
        namespaces = {'oai': 'http://www.openarchives.org/OAI/2.0/'}
        error_node = root.find('.//oai:error', namespaces)
        
        if error_node is not None:
            return error_node.text or error_node.get('code', 'Unknown Error')
            
    except ET.ParseError as e:
        return f"XML Parse Error: {e}"
        
    return None

def save_to_file(content: str, filename: str):
    """Saves the content to a local file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[+] Saved: {filename}")

def parse_mods_fields(xml_content: str) -> Dict:
    """Extracts key fields from MODS XML for tracer bullet verification."""
    ns = {"oai": OAI_NS, "mods": MODS_NS, "xml": "http://www.w3.org/XML/1998/namespace"}
    root = ET.fromstring(xml_content)
    mods = root.find(".//mods:mods", ns)
    if mods is None:
        return {"error": "No <mods> element found"}

    def text(path):
        el = mods.find(path, ns)
        return el.text.strip() if el is not None and el.text else None

    titles = {
        ti.get("{http://www.w3.org/XML/1998/namespace}lang", "?"):
            (ti.find("mods:title", ns).text or "").strip()
        for ti in mods.findall("mods:titleInfo", ns)
        if ti.find("mods:title", ns) is not None
    }

    authors = [
        f"{n.findtext('mods:namePart[@type=\"given\"]', namespaces=ns, default='')} "
        f"{n.findtext('mods:namePart[@type=\"family\"]', namespaces=ns, default='')}".strip()
        for n in mods.findall("mods:name[@type='personal']", ns)
    ]

    return {
        "titles": titles,
        "authors": authors,
        "language": text("mods:language/mods:languageTerm"),
        "date_issued": text("mods:originInfo/mods:dateIssued"),
        "publisher": text("mods:originInfo/mods:publisher"),
        "doi": next(
            (el.text for el in mods.findall("mods:identifier", ns)
             if el.get("type") == "doi"),
            None
        ),
        "journal": text("mods:relatedItem[@type='host']/mods:titleInfo/mods:title"),
        "abstract_tr": next(
            (el.text[:80] + "..." for el in mods.findall("mods:abstract", ns)
             if el.get("{http://www.w3.org/XML/1998/namespace}lang") == "tr-TR"),
            None
        ),
        "funders": [],
    }


def build_article(xml_content: str) -> ArticleMetadata:
    """Parses MODS XML and returns a validated ArticleMetadata instance."""
    raw = parse_mods_fields(xml_content)

    date_issued = raw.get("date_issued") or ""
    year_match = re.match(r"^(\d{4})", date_issued)
    if not year_match:
        raise ValueError(f"date_issued'den yıl çıkarılamadı: '{date_issued}'")

    return ArticleMetadata(
        title_tr=raw["titles"].get("tr-TR", ""),
        title_en=raw["titles"].get("en-US"),
        language=raw["language"] or "",
        publication_year=int(year_match.group(1)),
        identifier_doi=raw["doi"] or "",
        source_journal=raw["journal"] or "",
        abstract_tr=raw.get("abstract_tr"),
        authors=raw.get("authors", []),
        date_issued=date_issued,
        publisher=raw.get("publisher"),
        funders=[],
        ror_ids=[],
    )


def verify_outputs(filenames: List[str]) -> bool:
    """
    Verifies that the files exist, are not empty, and contain valid XML.
    """
    all_valid = True
    print("\n" + "="*40)
    print("VERIFICATION RESULTS")
    print("="*40)
    
    for filename in filenames:
        if not os.path.exists(filename):
            print(f"[-] {filename}: FILE MISSING")
            all_valid = False
            continue
            
        size = os.path.getsize(filename)
        if size == 0:
            print(f"[-] {filename}: EMPTY FILE")
            all_valid = False
            continue
            
        try:
            ET.parse(filename)
            print(f"[+] {filename}: VALID XML ({size} bytes)")
        except ET.ParseError as e:
            print(f"[-] {filename}: CORRUPT XML - {e}")
            all_valid = False
            
    return all_valid

def main():
    harvested_files = []
    
    for prefix in METADATA_PREFIXES:
        xml_content = fetch_metadata(prefix, IDENTIFIER)
        
        if not xml_content:
            print(f"[!!] Failed to retrieve {prefix}. Stopping.")
            break
            
        error = check_oai_errors(xml_content)
        if error:
            print(f"[!!] OAI-PMH Error ({prefix}): {error}. Stopping.")
            break
            
        filename = f"{prefix}_1674520.xml"
        save_to_file(xml_content, filename)
        harvested_files.append(filename)
        
    if harvested_files:
        success = verify_outputs(harvested_files)
        if success:
            print("\n--- PYDANTIC VALIDATION ---")
            with open(harvested_files[0], encoding="utf-8") as f:
                article = build_article(f.read())
            for k, v in article.model_dump().items():
                print(f"  {k}: {v}")
            print("\n[SUCCESS] Tracer Bullet + Pydantic validation completed successfully.")
        else:
            print("\n[FAILURE] One or more validations failed.")
    else:
        print("\n[FAILURE] No files were harvested.")

if __name__ == "__main__":
    main()
