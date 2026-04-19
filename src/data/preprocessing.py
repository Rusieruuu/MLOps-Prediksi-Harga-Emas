import os
import pandas as pd

# --- KONFIGURASI PATH ---
RAW_DATA_DIR = 'data/raw/'
PROCESSED_DATA_DIR = 'data/processed/'

os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

def preprocess_and_versioning():
    print("--- MEMULAI PRAPEMROSESAN & VERSIONING DATA ---")
    
    # --- PERBAIKAN: Langsung tembak ke satu file statis ---
    raw_filepath = os.path.join(RAW_DATA_DIR, "gold_data.csv")
    
    if not os.path.exists(raw_filepath):
        print(f"❌ Error: Tidak ditemukan {raw_filepath}.")
        return
        
    print(f"📦 Membaca data raw dari {raw_filepath}...")
    df = pd.read_csv(raw_filepath)
    
    # Pembersihan Standar
    df.dropna(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    
    # Deduplikasi
    baris_awal = len(df)
    df.drop_duplicates(subset='Date', keep='last', inplace=True)
    print(f"🧹 Membersihkan {baris_awal - len(df)} baris data duplikat.")
    
    # Sliding Window
    BATAS_DATA = 1000
    if len(df) > BATAS_DATA:
        df = df.tail(BATAS_DATA)
        print(f"✂️ Sliding Window aktif: Mengambil {BATAS_DATA} baris data terbaru.")
    
    # --- PERBAIKAN: Simpan ke satu master file saja ---
    master_filename = "gold_processed.csv"
    master_filepath = os.path.join(PROCESSED_DATA_DIR, master_filename)
    
    df.to_csv(master_filepath, index=False)
    
    print(f"✅ Preprocessing Selesai!")
    print(f"📍 File Bersih Tersimpan: {master_filepath} (Siap dilacak DVC)")
    print(f"📊 Total Data Bersih: {len(df)} baris.")

if __name__ == "__main__":
    preprocess_and_versioning()