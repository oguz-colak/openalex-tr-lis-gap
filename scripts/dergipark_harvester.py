import requests
import time
import os
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional

# Constants
BASE_URL = "https://dergipark.org.tr/api/public/oai/"
IDENTIFIER = "oai:dergipark.org.tr:article/1674520"
METADATA_PREFIXES = ["oai_dc", "oai_mods", "oai_marc"]
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
            print("\n[SUCCESS] Tracer Bullet test completed successfully.")
        else:
            print("\n[FAILURE] One or more validations failed.")
    else:
        print("\n[FAILURE] No files were harvested.")

if __name__ == "__main__":
    main()
