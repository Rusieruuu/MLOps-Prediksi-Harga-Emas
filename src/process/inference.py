import mlflow
import pandas as pd

# Targetkan database mlflow dan nama model
mlflow.set_tracking_uri("sqlite:///mlruns.db")
model_name = "Gold Prediction Model"
stage = "Production"

print(f"Mengunduh model '{model_name}' dengan stage '{stage}'...")
# Mengambil model secara dinamis berdasarkan stagenya
model = mlflow.pyfunc.load_model(model_uri=f"models:/{model_name}/{stage}")

# Membuat data dummy untuk simulasi testing
dummy_data = pd.DataFrame({
    'Open': [3950.5], 'High': [4000.0], 'Low': [3900.0], 'Volume': [150], 'Close': [3980.0],
    'Lag_1': [3960.0], 'Lag_7': [3900.0], 'MA_7': [3940.0], 'MA_30': [3850.0], 
    'Return': [0.005], 'Volatility': [0.012]
})

prediction = model.predict(dummy_data)
print("✅ Inferensi Berhasil!")
print(f"Prediksi Harga Emas Esok Hari: {prediction[0]:.2f}")