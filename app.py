from fastapi import FastAPI, Request
from fastapi.responses import Response
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
import os
import time
import psutil
from prometheus_client import (
    Counter, Histogram, Gauge,
    generate_latest, CONTENT_TYPE_LATEST
)

# ── Inisialisasi App ──────────────────────────────────────────
app = FastAPI(title="API Prediksi Harga Emas")

# ── Prometheus Metrics ────────────────────────────────────────
REQUEST_COUNT = Counter(
    "api_request_total",
    "Total jumlah request masuk",
    ["endpoint", "method", "status"]
)
REQUEST_LATENCY = Histogram(
    "api_request_latency_seconds",
    "Latensi request dalam detik",
    ["endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)
PREDICTION_VALUE = Gauge(
    "model_prediction_value",
    "Nilai prediksi harga emas terakhir"
)
CPU_USAGE = Gauge("system_cpu_usage_percent", "Penggunaan CPU (%)")
RAM_USAGE = Gauge("system_ram_usage_percent", "Penggunaan RAM (%)")

# ── Load Model ────────────────────────────────────────────────
model = None

def load_model():
    global model
    try:
        import pickle
        with open("mlruns/1/models/m-9b4236c6db3448a6ac7b1393b475e13a/artifacts/model.pkl", "rb") as f:
            model = pickle.load(f)
        print("✅ Model berhasil dimuat dari model.pkl!")
    except Exception as e:
        print(f"❌ Gagal load model: {e}")

@app.on_event("startup")
def startup_event():
    load_model()

# ── Endpoints ─────────────────────────────────────────────────
@app.get("/")
def home():
    tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", "http://localhost:5000")
    mlflow.set_tracking_uri(tracking_uri)
    try:
        client = MlflowClient()
        experiments = client.search_experiments()
        return {
            "status_api": "Aktif",
            "koneksi_mlflow": "SUKSES",
            "jumlah_eksperimen": len(experiments)
        }
    except Exception as e:
        return {"status_api": "Aktif", "koneksi_mlflow": f"GAGAL: {str(e)}"}

@app.post("/predict")
def predict(data: dict):
    start = time.time()
    status = "200"
    try:
        import pandas as pd
        df = pd.DataFrame([data])
        expected = ["Open","High","Low","Volume","Close",
                    "Lag_1","Lag_7","MA_7","MA_30","Return","Volatility"]
        df = df[expected]
        result = model.predict(df)[0]
        PREDICTION_VALUE.set(float(result))
        REQUEST_COUNT.labels("/predict", "POST", status).inc()
        REQUEST_LATENCY.labels("/predict").observe(time.time() - start)
        return {"prediction": float(result)}
    except Exception as e:
        status = "500"
        REQUEST_COUNT.labels("/predict", "POST", status).inc()
        return {"error": str(e)}

@app.get("/metrics")
def metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    RAM_USAGE.set(psutil.virtual_memory().percent)
    REQUEST_COUNT.labels("/metrics", "GET", "200").inc()
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/health")
def health():
    return {"status": "ok"}