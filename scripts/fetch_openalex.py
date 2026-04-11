import os
import json
import time
import requests
import logging
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

# --- CONFIGURATION ---
MAILTO = "oguzcan@example.com"  # placeholder mailto for OpenAlex Polite Pool
BASE_URL = "https://api.openalex.org/works"

# Source IDs for the 6 LIS journals (Using full OpenAlex URIs)
SOURCE_IDS = [
    "https://openalex.org/s2736521800" # Bilgi Dünyası
    # Add other IDs here as they become available
]

FILTER = f"primary_location.source.id:{'|'.join(SOURCE_IDS)}"
DATA_FILE = "data/raw/openalex_bby_works_full.json"
STATE_FILE = "data/raw/openalex_state.json"

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("openalex_fetch.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- FUNCTIONS ---

def save_data(records):
    """Appends records to the JSON file safely."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
    
    with open(DATA_FILE, 'r+', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
        
        # Optimization: remove abstract_inverted_index
        for record in records:
            record.pop('abstract_inverted_index', None)
        
        data.extend(records)
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.truncate()

def save_state(cursor):
    """Saves the current cursor to a state file."""
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump({"cursor": cursor}, f)

def load_state():
    """Loads the last valid cursor from the state file."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)
            return state.get("cursor", "*")
    return "*"

@retry(
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(10),
    retry=retry_if_exception_type((requests.exceptions.RequestException, requests.exceptions.HTTPError)),
    reraise=True
)
def fetch_page(cursor):
    """Fetches a single page of results from OpenAlex."""
    params = {
        "filter": FILTER,
        "cursor": cursor,
        "per_page": 200,
        "mailto": MAILTO
    }
    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()

def main():
    # Ensure raw data directory exists
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    cursor = load_state()
    logger.info(f"Starting fetch with cursor: {cursor}")
    
    total_fetched = 0
    
    while cursor:
        try:
            data = fetch_page(cursor)
            results = data.get("results", [])
            next_cursor = data.get("meta", {}).get("next_cursor")
            
            if not results:
                logger.info("No more results found.")
                break
            
            # Save data and state
            save_data(results)
            save_state(next_cursor)
            
            total_fetched += len(results)
            logger.info(f"Fetched {len(results)} records (Total: {total_fetched}). Next cursor: {next_cursor}")
            
            # Stop if no next cursor
            if not next_cursor or next_cursor == cursor:
                break
                
            cursor = next_cursor
            
            # Small polite delay
            time.sleep(0.1)
            
        except Exception as e:
            logger.error(f"Fatal error during fetching: {e}")
            raise

    logger.info(f"Job completed. Total records saved: {total_fetched}")

if __name__ == "__main__":
    main()
