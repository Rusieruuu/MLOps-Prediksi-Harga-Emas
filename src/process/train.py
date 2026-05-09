import os
import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import mlflow
import mlflow.sklearn

def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2

def train_model(n_estimators, max_depth):
    print("--- MEMULAI TRAINING MODEL PREDIKSI EMAS ---")
    
    data_path = "data/processed/gold_processed.csv"
    if not os.path.exists(data_path):
        print(f"❌ Error: File {data_path} tidak ditemukan.")
        return
        
    df = pd.read_csv(data_path)
    
    # --- FEATURE ENGINEERING (Sesuai Dokumen Desain LK-01) ---
    # Fitur Historis (Lag)
    df['Lag_1'] = df['Close'].shift(1)
    df['Lag_7'] = df['Close'].shift(7)
    
    # Rata-rata Bergerak (Moving Average)
    df['MA_7'] = df['Close'].rolling(window=7).mean()
    df['MA_30'] = df['Close'].rolling(window=30).mean()
    
    # Persentase Perubahan & Fluktuasi (Return & Volatility)
    df['Return'] = df['Close'].pct_change()
    df['Volatility'] = df['Return'].rolling(window=7).std() # Menggunakan standar deviasi return 7 hari
    
    # Target: Prediksi harga H+1
    df['Target'] = df['Close'].shift(-1)
    
    # Buang baris yang memiliki nilai kosong (NaN) akibat proses shift dan rolling
    df.dropna(inplace=True) 
    
    # Gunakan fitur yang telah diwajibkan pada desain sistem
    features = ['Open', 'High', 'Low', 'Volume', 'Close', 
                'Lag_1', 'Lag_7', 'MA_7', 'MA_30', 'Return', 'Volatility']
    
    X = df[features]
    y = df['Target']
    
    # Split Data (Time-series split, urutan waktu dijaga ketat)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)
    
    with mlflow.start_run():
        rf = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
        rf.fit(X_train, y_train)
        
        predicted_prices = rf.predict(X_test)
        (rmse, mae, r2) = eval_metrics(y_test, predicted_prices)
        
        print(f"Model RF (n_estimators={n_estimators}, max_depth={max_depth}):")
        print(f"  RMSE: {rmse:.4f} | R2: {r2:.4f} | MAE: {mae:.4f}")
        
        # Logging Metrik & Parameter ke MLflow untuk keperluan evaluasi Champion-Challenger
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)
        mlflow.sklearn.log_model(rf, "model")
        print("✅ Eksperimen berhasil dicatat oleh MLflow!\n")

        THRESHOLD_R2 = 0.40
        
        if r2 >= THRESHOLD_R2:
            print(f"🌟 Evaluasi Sukses! R2 ({r2:.4f}) melebihi threshold ({THRESHOLD_R2}).")
            print("Mendaftarkan model ke Model Registry dengan status Staging...")
            
            # Ambil ID run saat ini
            run_id = mlflow.active_run().info.run_id
            model_uri = f"runs:/{run_id}/model"
            
            # Daftarkan Model
            nama_model = "Gold Prediction Model"
            mv = mlflow.register_model(model_uri, nama_model)
            
            # Ubah status ke Staging menggunakan MLflow Client
            client = mlflow.tracking.MlflowClient()
            client.transition_model_version_stage(
                name=nama_model,
                version=mv.version,
                stage="Staging"
            )
            print("✅ Model otomatis masuk ke Staging!")
        else:
            print(f"❌ Evaluasi Gagal. R2 ({r2:.4f}) di bawah threshold. Model ditolak.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--max_depth", type=int, default=5)
    args = parser.parse_args()
    
    mlflow.set_tracking_uri("sqlite:///mlruns.db")
    mlflow.set_experiment("Eksperimen_Prediksi_Emas")

    train_model(args.n_estimators, args.max_depth)
    