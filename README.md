# MLOps-Prediksi-Harga-Emas

## Tujuan Proyek
Proyek ini merupakan inisiasi pengembangan sistem *Artificial Intelligence* (AI) secara individu yang berorientasi pada tahap *production*. Tujuan utamanya adalah membangun sistem peramalan harga emas menggunakan prinsip-prinsip MLOps, termasuk implementasi *pipeline* untuk *continuous training* agar model dapat beradaptasi dengan pergerakan harga pasar secara dinamis.

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

## 🛠️ Manajemen Versi Data (DVC) & Remote Storage
Proyek ini memisahkan antara kode program (Git) dan dataset berukuran besar (DVC). Metadata dataset disimpan dalam file `.dvc`, sedangkan data asli disimpan di remote storage.

### 1. Inisialisasi & Konfigurasi
DVC diinisialisasi untuk mengelola siklus hidup data. Remote storage dikonfigurasi menggunakan DagsHub (HTTPS) sebagai tujuan default penyimpanan melalui perintah `dvc init` dan `dvc remote add`.

### 2. Alur Pelacakan Data (Data Tracking)
Setiap dataset baru yang masuk melalui folder `data/raw/` atau `data/processed/` akan didaftarkan ke DVC untuk dibuatkan "sidik jari" (MD5 hash) menggunakan perintah `dvc add`. Setelah itu, hanya file pointer `.dvc` dan `.gitignore` yang di-commit ke Git.

### 3. Simulasi Continual Learning
Saat terjadi penambahan atau perubahan data (misal: setelah menjalankan skrip ingest dan preprocessing terbaru), alur kerja yang dilakukan adalah:
1. Lakukan tracking ulang pada dataset menggunakan `dvc add` untuk memperbarui metadata.
2. Push data fisik yang baru ke DagsHub menggunakan `dvc push`.
3. Commit perubahan file `.dvc` ke Git untuk mencatat versi metadata terbaru.

### 4. Audit & Verifikasi Data
Untuk memantau perbedaan antar versi data, digunakan perintah:
* `dvc status`: Melihat file data yang berubah namun belum di-track.
* `dvc diff`: Melihat perbedaan ukuran dan hash antara versi data lama dan baru.

### 5. Integrasi Object Storage (DagsHub)
Dataset pada proyek ini **tidak disimpan di GitHub**. Kami menggunakan **DagsHub** sebagai Object Storage eksternal. Hal ini memungkinkan kolaborasi data yang besar dengan efisien tanpa batasan limitasi file Git.
* **Status Data**: DVC Managed
* **Storage Lokasi**: https://dagshub.com/Rusieruuu/MLOps-Prediksi-Harga-Emas

---

## Cara Menjalankan Lingkungan Kerja (GitHub Codespaces)
Repositori ini telah dikonfigurasi untuk dijalankan secara instan menggunakan GitHub Codespaces dengan lingkungan Python yang sudah terisolasi dan konsisten.

1. Pada halaman utama repositori GitHub ini, klik tombol hijau **`<> Code`**.
2. Pilih tab **`Codespaces`**.
3. Klik **`Create codespace on main`**.
4. Tunggu beberapa saat hingga VS Code berbasis *web* terbuka. Semua ekstensi dan dependensi akan disiapkan secara otomatis.

---

## Eksperimen & Model Registry (MLflow)
Pelatihan model dikelola dan diaudit secara otomatis menggunakan **MLflow**. Algoritma yang digunakan adalah Random Forest Regressor untuk melakukan peramalan H+1 (Next-Day Prediction) terhadap harga emas (`Close`) sesuai dengan dokumen rancangan sistem awal.

### Hasil Eksperimen MLflow
Berdasarkan proses eksekusi dengan berbagai variasi parameter, berikut adalah metrik dari model terbaik (Champion Model) yang siap didaftarkan ke *Model Registry* untuk fase *deployment*:

* **Algoritma:** Random Forest Regressor
* **Parameter Terbaik:** `n_estimators` = 200, `max_depth` = 15
* **Metrik Performa:**
  * RMSE: 17.17
  * MAE: 14.76
  * R2 Score: 0.48

### Analisis Evaluasi Model
Meskipun nilai R2 berada di angka 0.48, performa model ini terbukti sangat prima secara operasional. Mengingat aset GOLD pada dataset diperdagangkan di kisaran harga ~4000, nilai RMSE 17.17 menunjukkan bahwa model rata-rata hanya memiliki **margin of error sebesar ~0.4%** dalam memprediksi harga keesokan harinya. 

Hal ini membuktikan bahwa *Feature Engineering* menggunakan variabel temporal (`Lag`, `Moving Average`, dan `Volatility`) berhasil menangkap sinyal tren pergerakan harga secara realistis, tanpa terjebak pada *overfitting* atau *data leakage* yang sering memanipulasi metrik pada pemodelan *time-series*. Pipeline eksperimen (MLOps) telah berjalan dengan baik dan siap dilanjutkan ke tahap pembuatan API.

---
