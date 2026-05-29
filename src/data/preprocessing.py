import os
import pandas as pd

RAW_DATA_DIR = 'data/raw/'
PROCESSED_DATA_DIR = 'data/processed/'
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

def preprocess_and_versioning():
    print("--- MEMULAI PRAPEMROSESAN & VERSIONING DATA ---")
    
    raw_filepath = os.path.join(RAW_DATA_DIR, "gold_data.csv")
    if not os.path.exists(raw_filepath):
        print(f"❌ Error: Tidak ditemukan {raw_filepath}.")
        return
        
    print(f"📦 Membaca data raw dari {raw_filepath}...")
    df = pd.read_csv(raw_filepath)
    
    df.dropna(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    
    baris_awal = len(df)
    df.drop_duplicates(subset='Date', keep='last', inplace=True)
    print(f"🧹 Membersihkan {baris_awal - len(df)} baris data duplikat.")
    
    BATAS_DATA = 1000
    if len(df) > BATAS_DATA:
        df = df.tail(BATAS_DATA)
        print(f"✂️ Sliding Window aktif: Mengambil {BATAS_DATA} baris data terbaru.")
    
    # Feature Engineering
    df['Lag_1'] = df['Close'].shift(1)
    df['Lag_7'] = df['Close'].shift(7)
    df['MA_7'] = df['Close'].rolling(window=7).mean()
    df['MA_30'] = df['Close'].rolling(window=30).mean()
    df['Return'] = df['Close'].pct_change()
    df['Volatility'] = df['Return'].rolling(window=7).std()
    df.dropna(inplace=True)
    print(f"✅ Feature engineering selesai: {len(df.columns)} kolom.")
    
    master_filename = "gold_processed.csv"
    master_filepath = os.path.join(PROCESSED_DATA_DIR, master_filename)
    df.to_csv(master_filepath, index=False)
    
    print(f"✅ Preprocessing Selesai!")
    print(f"📍 File Bersih Tersimpan: {master_filepath}")
    print(f"📊 Total Data Bersih: {len(df)} baris.")

if __name__ == "__main__":
    preprocess_and_versioning()
