import pandas as pd
import numpy as np

print("🔄 Membuat data simulasi drift...")

df = pd.read_csv("data/processed/gold_processed.csv")
df['Date'] = pd.to_datetime(df['Date'])
df.sort_values('Date', inplace=True)

# Simpan backup
df.to_csv("data/processed/gold_processed_backup.csv", index=False)

# Shift data 30 baris terakhir: naikkan harga 40% (simulasi drift ekstrem)
df_drift = df.copy()
last_30 = df_drift.index[-30:]
for col in ['Open', 'High', 'Low', 'Close']:
    df_drift.loc[last_30, col] = df_drift.loc[last_30, col] * 1.4

df_drift.to_csv("data/processed/gold_processed.csv", index=False)
print("✅ Data drift berhasil disimulasikan!")
print(f"   Harga Close sebelum: {df['Close'].iloc[-1]:.2f}")
print(f"   Harga Close sesudah: {df_drift['Close'].iloc[-1]:.2f}")
print("\nJalankan: python src/monitoring/check_drift.py")
