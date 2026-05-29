import pandas as pd
import requests
import time
import random

df = pd.read_csv("data/processed/gold_processed.csv")
features = ["Open","High","Low","Volume","Close","Lag_1","Lag_7","MA_7","MA_30","Return","Volatility"]
df = df[features].dropna().tail(50)

ports = [8000, 8001, 8002]

print("🚀 Memulai simulasi traffic ke 3 replika...")
for i, (_, row) in enumerate(df.iterrows()):
    port = ports[i % 3]
    payload = row.to_dict()
    try:
        r = requests.post(f"http://localhost:{port}/predict", json=payload)
        print(f"[Port {port}] Request {i+1}: {r.json()}")
    except Exception as e:
        print(f"[Port {port}] Error: {e}")
    time.sleep(0.3)

print("✅ Simulasi selesai! Buka Grafana dan refresh.")
