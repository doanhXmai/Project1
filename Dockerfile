# ----- Stage 1: Base để cài đặt dependencies -----
FROM python:3.11-slim AS base

ENV DEBIAN_FRONTEND=noninteractive

# Cài các package hệ thống + ffmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Tạo thư mục app
WORKDIR /app

# Copy requirements trước để tối ưu cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt


# ----- Stage 2: Runtime -----
FROM python:3.11-slim

WORKDIR /app

# Copy ffmpeg từ base
COPY --from=base /usr/bin/ffmpeg /usr/bin/ffmpeg

# Copy toàn bộ code vào /app
COPY . .

# Copy environment file nếu muốn
# (Railway/Render/AWS sẽ override ENV nên vẫn OK)
# COPY .env .env

EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
