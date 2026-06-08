import pandas as pd
import numpy as np
import sys

def check_drift(reference_path="data/processed/gold_processed.csv", threshold=0.2):
    print("--- CEK DATA DRIFT ---")
    
    df = pd.read_csv(reference_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)

    # Threshold berbeda per fitur
    thresholds = {
        'Open': 0.20,
        'High': 0.20,
        'Low':  0.20,
        'Close': 0.20,
        'Volume': 0.50  # Volume lebih volatile, threshold lebih tinggi
    }
    features = list(thresholds.keys())

    n = len(df)
    if n < 60:
        print("⚠️ Data kurang dari 60 baris, skip drift check.")
        sys.exit(0)

    ref = df[features].iloc[-60:-30]
    cur = df[features].iloc[-30:]

    drift_detected = False
    print(f"\n{'Fitur':<12} {'Mean Ref':>10} {'Mean Cur':>10} {'Drift %':>10} {'Threshold':>10} {'Status':>10}")
    print("-" * 65)

    for col in features:
        mean_ref = ref[col].mean()
        mean_cur = cur[col].mean()
        if mean_ref == 0:
            continue
        drift_pct = abs(mean_cur - mean_ref) / abs(mean_ref)
        thr = thresholds[col]
        status = "⚠️ DRIFT" if drift_pct > thr else "✅ OK"
        if drift_pct > thr:
            drift_detected = True
        print(f"{col:<12} {mean_ref:>10.2f} {mean_cur:>10.2f} {drift_pct*100:>9.1f}% {thr*100:>9.0f}% {status:>10}")

    print("-" * 65)
    if drift_detected:
        print(f"\n🚨 DATA DRIFT TERDETEKSI!")
        print("   → Retraining diperlukan!")
        sys.exit(1)
    else:
        print(f"\n✅ Tidak ada drift signifikan.")
        sys.exit(0)

if __name__ == "__main__":
    check_drift()
