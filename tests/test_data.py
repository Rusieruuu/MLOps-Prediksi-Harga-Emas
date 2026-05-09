import os
import pandas as pd

def test_data_exists():
    """Memastikan file data processed tersedia"""
    assert os.path.exists("data/processed/gold_processed.csv"), "File data tidak ditemukan!"

def test_kolom_wajib_ada():
    """Memastikan struktur kolom data dasar sudah benar sebelum masuk ke train.py"""
    df = pd.read_csv("data/processed/gold_processed.csv")
    kolom_wajib = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    
    for kolom in kolom_wajib:
        assert kolom in df.columns, f"Kolom {kolom} hilang dari dataset!"