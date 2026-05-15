from fastapi import FastAPI
import mlflow
from mlflow.tracking import MlflowClient
import os

app = FastAPI(title="API Prediksi Harga Emas")

@app.get("/")
def home():
    # Menyiapkan alamat MLflow dari Docker Compose
    tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", "http://localhost:5000")
    mlflow.set_tracking_uri(tracking_uri)
    
    # Mencoba menarik data dari MLflow Server
    try:
        client = MlflowClient()
        experiments = client.search_experiments()
        return {
            "status_api": "Aktif",
            "koneksi_mlflow": "SUKSES: Berhasil menarik data dari MLflow Server di dalam jaringan Docker!",
            "jumlah_eksperimen": len(experiments)
        }
    except Exception as e:
        return {
            "status_api": "Aktif",
            "koneksi_mlflow": f"GAGAL: {str(e)}"
        }