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

## Cara Menjalankan Lingkungan Kerja (GitHub Codespaces)
Repositori ini telah dikonfigurasi untuk dijalankan secara instan menggunakan GitHub Codespaces dengan lingkungan Python yang sudah terisolasi dan konsisten.

1. Pada halaman utama repositori GitHub ini, klik tombol hijau **`<> Code`**.
2. Pilih tab **`Codespaces`**.
3. Klik **`Create codespace on main`**.
4. Tunggu beberapa saat hingga VS Code berbasis *web* terbuka. Semua ekstensi dan dependensi akan disiapkan secara otomatis.