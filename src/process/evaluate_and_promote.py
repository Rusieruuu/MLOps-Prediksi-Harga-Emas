import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import argparse
import sys

def evaluate_and_promote(tracking_uri="sqlite:///mlruns.db"):
    mlflow.set_tracking_uri(tracking_uri)
    client = MlflowClient()
    model_name = "Gold Prediction Model"

    # Load data test
    df = pd.read_csv("data/processed/gold_processed.csv")
    df['Lag_1'] = df['Close'].shift(1)
    df['Lag_7'] = df['Close'].shift(7)
    df['MA_7']  = df['Close'].rolling(7).mean()
    df['MA_30'] = df['Close'].rolling(30).mean()
    df['Return'] = df['Close'].pct_change()
    df['Volatility'] = df['Return'].rolling(7).std()
    df['Target'] = df['Close'].shift(-1)
    df.dropna(inplace=True)

    features = ['Open','High','Low','Volume','Close',
                'Lag_1','Lag_7','MA_7','MA_30','Return','Volatility']
    X = df[features].tail(100)
    y = df['Target'].tail(100)

    # Ambil model Production (lama)
    try:
        model_prod = mlflow.sklearn.load_model(f"models:/{model_name}/Production")
        pred_prod  = model_prod.predict(X)
        r2_prod    = r2_score(y, pred_prod)
        print(f"📊 Model Production R²: {r2_prod:.4f}")
    except Exception as e:
        print(f"⚠️ Tidak ada model Production: {e}")
        r2_prod = -999

    # Ambil model terbaru (Staging)
    try:
        model_new = mlflow.sklearn.load_model(f"models:/{model_name}/Staging")
        pred_new  = model_new.predict(X)
        r2_new    = r2_score(y, pred_new)
        rmse_new  = np.sqrt(mean_squared_error(y, pred_new))
        mae_new   = mean_absolute_error(y, pred_new)
        print(f"📊 Model Baru (Staging) R²: {r2_new:.4f}")
    except Exception as e:
        print(f"❌ Tidak ada model Staging: {e}")
        sys.exit(1)

    # Komparasi & Promosi
    print(f"\n{'='*50}")
    print(f"Perbandingan Model:")
    print(f"  Production R²  : {r2_prod:.4f}")
    print(f"  Staging R²     : {r2_new:.4f}")
    print(f"  RMSE (baru)    : {rmse_new:.4f}")
    print(f"  MAE (baru)     : {mae_new:.4f}")
    print(f"{'='*50}")

    THRESHOLD = 0.4
    if r2_new > r2_prod and r2_new >= THRESHOLD:
        versions = client.search_model_versions(f"name='{model_name}'")
        staging_versions = [v for v in versions if v.current_stage == "Staging"]
        if staging_versions:
            latest = max(staging_versions, key=lambda v: int(v.version))
            client.transition_model_version_stage(
                name=model_name,
                version=latest.version,
                stage="Production",
                archive_existing_versions=True
            )
            print(f"✅ Model v{latest.version} dipromosikan ke Production!")
            print(f"   R² meningkat: {r2_prod:.4f} → {r2_new:.4f}")
        sys.exit(0)
    else:
        print(f"❌ Model baru tidak lebih baik. Tetap pakai Production.")
        if r2_new < THRESHOLD:
            print(f"   R² ({r2_new:.4f}) di bawah threshold ({THRESHOLD})")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tracking-uri", default="sqlite:///mlruns.db")
    args = parser.parse_args()
    evaluate_and_promote(args.tracking_uri)
