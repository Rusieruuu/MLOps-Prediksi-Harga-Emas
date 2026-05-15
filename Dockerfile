# 1. Pakai Python 3.12 versi ringan
FROM python:3.12-slim

# 2. Bikin folder khusus di dalam kontainer
WORKDIR /app

# 3. Salin file requirements kamu
COPY requirements.txt .

# 4. Install library yang dibutuhkan, ditambah FastAPI agar API bisa jalan
RUN pip install --no-cache-dir -r requirements.txt fastapi uvicorn

# 5. Salin semua file kodemu ke dalam kontainer
COPY . .

# 6. Buka gerbang komunikasi di port 8000
EXPOSE 8000

# 7. Perintah menyalakan API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]