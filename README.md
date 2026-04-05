# MLOps-Prediksi-Harga-Emas

## Tujuan Proyek
Proyek ini merupakan inisiasi pengembangan sistem *Artificial Intelligence* (AI) secara individu yang berorientasi pada tahap *production*. Tujuan utamanya adalah membangun sistem peramalan harga emas (XAU/USD) menggunakan prinsip-prinsip MLOps, termasuk implementasi *pipeline* untuk *continuous training* agar model dapat beradaptasi dengan pergerakan harga pasar secara dinamis.

## Struktur Direktori
Proyek ini diorganisasikan menggunakan konvensi standar industri untuk memastikan kerapian dan skalabilitas:

* `config/` : Berisi file konfigurasi untuk parameter sistem.
* `data/` : Tempat penyimpanan data historis (terbagi menjadi data `raw/` dan `processed/`).
* `models/` : Direktori untuk menyimpan model *machine learning* yang telah dilatih.
* `notebooks/` : Berisi Jupyter Notebooks untuk eksperimen awal dan Exploratory Data Analysis (EDA).
* `src/` : *Source code* utama untuk pemrosesan data, *feature engineering*, dan *pipeline* pelatihan model.

---

## ⚙️ Implementasi Pipeline Data
Bagian ini mengelola alur data otomatis dari pengambilan hingga siap digunakan oleh model AI untuk mendukung konsep *Continual Learning*.

### 1. Ingest Data Mentah (`ingest_data.py`)
Skrip ini bertugas menarik data terbaru secara otomatis dari API Alpha Vantage.
* **Aset:** Menggunakan ticker **GLD** (SPDR Gold Shares) sebagai proksi harga emas untuk mendapatkan data volume transaksi yang valid bagi model ML.
* **Mekanisme:** Menarik 100 baris data terbaru harian secara otomatis.
* **Non-Destruktif:** Nama file menggunakan *full timestamp* (`gold_raw_YYYYMMDD_HHMMSS.csv`) agar data historis tetap tersimpan dan tidak tertimpa.
* **Eksekusi:** `python src/data/ingest_data.py`

### 2. Automasi Prapemrosesan (`preprocessing.py`)
Skrip ini mengolah seluruh file mentah menjadi dataset tunggal yang bersih dan terstandarisasi.
* **Deduplikasi:** Mengeliminasi data dengan tanggal yang sama akibat pengambilan berulang.
* **Sliding Window:** Membatasi dataset pada **1000 baris terbaru** untuk memastikan model hanya belajar dari tren pasar terkini.
* **Versioning:** Menghasilkan file **Master** (`gold_master_processed.csv`) untuk pelatihan model dan file **Versi** unik ber-timestamp untuk kebutuhan audit eksperimen.
* **Eksekusi:** `python src/data/preprocessing.py`

---

## Cara Menjalankan Lingkungan Kerja (GitHub Codespaces)
Repositori ini telah dikonfigurasi untuk dijalankan secara instan menggunakan GitHub Codespaces dengan lingkungan Python yang sudah terisolasi dan konsisten.

1. Pada halaman utama repositori GitHub ini, klik tombol hijau **`<> Code`**.
2. Pilih tab **`Codespaces`**.
3. Klik **`Create codespace on main`**.
4. Tunggu beberapa saat hingga VS Code berbasis *web* terbuka. Semua ekstensi dan dependensi akan disiapkan secara otomatis.