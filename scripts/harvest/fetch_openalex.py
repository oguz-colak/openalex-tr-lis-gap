import os
import json
import time
import requests
import logging
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from dotenv import load_dotenv

# .env dosyasındaki API anahtarını yükle
load_dotenv()

# --- CONFIGURATION ---
API_KEY = os.environ.get('OPENALEX_API_KEY')
MAILTO = "oguzcan@example.com"  # OpenAlex Polite Pool için e-posta
BASE_URL = "https://api.openalex.org/works"

# 6 Dergi ve varyasyonları için OpenAlex Source ID'leri
SOURCE_IDS = [
    "https://openalex.org/S4210169130", # Bilgi ve Belge Araştırmaları
    "https://openalex.org/S2737140681", # Türk Kütüphaneciliği
    "https://openalex.org/S4210200535", # Arşiv Dünyası
    "https://openalex.org/S4210235296", # Bilgi Yönetimi (Yayıncı hatası olan)
    "https://openalex.org/S2736521800", # Bilgi Dünyası (Ana Kayıt)
    "https://openalex.org/S4306401264", # Bilgi Dünyası (Parçalanmış Kayıt 1)
    "https://openalex.org/S4306401982", # Bilgi Dünyası (Parçalanmış Kayıt 2)
    "https://openalex.org/S4210236601"  # LAMRe Journal
]

# KRİTİK: 'primary_location' yerine tüm 'locations' dizisini tarıyoruz ki hayalet veriler kaçmasın.
FILTER = f"locations.source.id:{'|'.join(SOURCE_IDS)}"
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
        
        # Optimization: remove abstract_inverted_index to save space
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
    
    # Eğer API Key varsa isteğe ekle (Limitleri genişletmek için)
    if API_KEY:
        params["api_key"] = API_KEY

    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()

def main():
    # Ensure raw data directory exists
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    # State dosyasını sıfırla (Temiz çekim için)
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
        
    cursor = "*"
    logger.info("Mevcut veri temizlendi. API Key ile yeni çekim başlatılıyor...")
    
    total_fetched = 0
    
    while cursor:
        try:
            data = fetch_page(cursor)
            results = data.get("results", [])
            next_cursor = data.get("meta", {}).get("next_cursor")
            
            if not results:
                logger.info("Başka sonuç bulunamadı.")
                break
            
            # Save data and state
            save_data(results)
            save_state(next_cursor)
            
            total_fetched += len(results)
            logger.info(f"{len(results)} kayıt çekildi (Toplam: {total_fetched}). Sonraki imleç: {next_cursor}")
            
            # Stop if no next cursor
            if not next_cursor or next_cursor == cursor:
                break
                
            cursor = next_cursor
            
            # API Key olduğu için bekleme süresini optimize edebiliriz
            time.sleep(0.1)
            
        except Exception as e:
            logger.error(f"Veri çekilirken kritik hata: {e}")
            raise

    logger.info(f"İşlem tamamlandı. Kaydedilen toplam BBY makalesi: {total_fetched}")

if __name__ == "__main__":
    main()