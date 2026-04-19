import os
import pandas as pd
import requests

# --- KONFIGURASI ---
RAW_DATA_DIR = 'data/raw/'
os.makedirs(RAW_DATA_DIR, exist_ok=True)

API_KEY = "45BR4FHJM2P78TSK" 
SYMBOL = "GLD"

def fetch_gold_data():
    print(f"--- MEMULAI DATA INGESTION: {SYMBOL} ---")
    
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": SYMBOL,
        "outputsize": "compact", 
        "apikey": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if "Error Message" in data:
            print(f"❌ API Error: {data['Error Message']}")
            return
        elif "Information" in data:
            print(f"⚠️ API Info/Limit: {data['Information']}")
            return

        ts = data.get("Time Series (Daily)")
        if not ts:
            print("❌ Gagal mengambil data. Struktur JSON tidak sesuai.")
            return

        df = pd.DataFrame.from_dict(ts, orient="index")
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        df.index.name = 'Date'
        df.reset_index(inplace=True)
        
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            df[col] = pd.to_numeric(df[col])
        df['Date'] = pd.to_datetime(df['Date'])
        
        df.sort_values('Date', inplace=True)

        # --- PERBAIKAN UNTUK DVC: Gunakan nama file statis ---
        filename = "gold_data.csv"
        filepath = os.path.join(RAW_DATA_DIR, filename)
        
        df.to_csv(filepath, index=False)
        print(f"✅ BERHASIL: Menarik {len(df)} baris data.")
        print(f"📍 Tersimpan di: {filepath} (Siap dilacak DVC)")

    except Exception as e:
        print(f"❌ Terjadi kesalahan teknis: {e}")

if __name__ == "__main__":
    fetch_gold_data()