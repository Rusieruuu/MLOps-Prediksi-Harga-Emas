import os
import pandas as pd
import requests
from datetime import datetime

# --- KONFIGURASI ---
RAW_DATA_DIR = 'data/raw/'
os.makedirs(RAW_DATA_DIR, exist_ok=True)

# Gunakan API Key Alpha Vantage Anda
API_KEY = "45BR4FHJM2P78TSK" 
SYMBOL = "GLD" # Ticker untuk Emas (ETF)

def fetch_gold_data():
    print(f"--- MEMULAI DATA INGESTION: {SYMBOL} ---")
    
    # URL dan Parameter API
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": SYMBOL,
        "outputsize": "compact", # Jatah gratis: memberikan 100 baris terbaru
        "apikey": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        # Validasi Error dari API
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

        # Transformasi ke DataFrame
        df = pd.DataFrame.from_dict(ts, orient="index")
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        df.index.name = 'Date'
        df.reset_index(inplace=True)
        
        # Konversi tipe data ke numerik dan tanggal
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            df[col] = pd.to_numeric(df[col])
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Urutkan dari data lama ke baru
        df.sort_values('Date', inplace=True)

        # Simpan file mentah dengan Timestamp (Agar tidak destruktif)
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gold_raw_{current_time}.csv"
        filepath = os.path.join(RAW_DATA_DIR, filename)
        
        df.to_csv(filepath, index=False)
        print(f"✅ BERHASIL: Menarik {len(df)} baris data.")
        print(f"📍 Tersimpan di: {filepath}")

    except Exception as e:
        print(f"❌ Terjadi kesalahan teknis: {e}")

if __name__ == "__main__":
    fetch_gold_data()