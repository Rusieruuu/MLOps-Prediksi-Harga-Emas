# Simpan sebagai: src/data/preprocess.py

import os
import glob
import pandas as pd
from datetime import datetime

# --- KONFIGURASI PATH ---
RAW_DATA_DIR = 'data/raw/'
PROCESSED_DATA_DIR = 'data/processed/'

# Pastikan folder tujuan sudah ada
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

def preprocess_and_versioning():
    print("--- MEMULAI PRAPEMROSESAN & VERSIONING DATA ---")
    
    # 1. Mengambil seluruh file CSV hasil tarikan API di folder raw
    all_files = glob.glob(os.path.join(RAW_DATA_DIR, "*.csv"))
    if not all_files:
        print("❌ Error: Tidak ditemukan file data mentah di folder data/raw/.")
        return
        
    print(f"📦 Menggabungkan {len(all_files)} file raw...")
    
    # 2. Penggabungan Data (Merging)
    df_list = [pd.read_csv(f) for f in all_files]
    df_merged = pd.concat(df_list, ignore_index=True)
    
    # 3. Pembersihan Standar
    df_merged.dropna(inplace=True)
    df_merged['Date'] = pd.to_datetime(df_merged['Date'])
    df_merged.sort_values('Date', inplace=True)
    
    # 4. Deduplikasi (Menghapus Tanggal yang Sama)
    # Sangat penting karena pengambilan data 'compact' setiap hari pasti tumpang tindih
    baris_awal = len(df_merged)
    df_merged.drop_duplicates(subset='Date', keep='last', inplace=True)
    print(f"🧹 Membersihkan {baris_awal - len(df_merged)} baris data duplikat.")
    
    # 5. Implementasi Sliding Window (Maksimal 1000 Data Terbaru)
    # Menjamin model hanya belajar dari tren harga emas terkini
    BATAS_DATA = 1000
    if len(df_merged) > BATAS_DATA:
        df_merged = df_merged.tail(BATAS_DATA)
        print(f"✂️ Sliding Window aktif: Mengambil {BATAS_DATA} baris data terbaru.")
    
    # 6. Penyimpanan dengan Full Timestamp (Versioning)
    # Menggunakan format TahunBulanTanggal_JamMenitDetik agar selalu UNIK
    timestamp_unik = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Nama file versi (untuk arsip/audit)
    version_filename = f"gold_processed_{timestamp_unik}.csv"
    version_filepath = os.path.join(PROCESSED_DATA_DIR, version_filename)
    
    # Nama file master (selalu tetap untuk input Model Training)
    master_filename = "gold_master_processed.csv"
    master_filepath = os.path.join(PROCESSED_DATA_DIR, master_filename)
    
    # Simpan kedua file
    df_merged.to_csv(version_filepath, index=False)
    df_merged.to_csv(master_filepath, index=False)
    
    print(f"✅ File Versi Tersimpan: {version_filepath}")
    print(f"📍 Master File Terupdate: {master_filepath}")
    print(f"📊 Total Data Bersih: {len(df_merged)} baris.")

if __name__ == "__main__":
    preprocess_and_versioning()