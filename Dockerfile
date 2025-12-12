# ----- Stage 1: Builder (Dùng để build và cài gói) -----
FROM python:3.11-slim AS builder

ENV DEBIAN_FRONTEND=noninteractive

# Tạo thư mục app
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# 1. Tạo môi trường ảo (Virtual Environment) tại /opt/venv
# 2. Kích hoạt và cài đặt dependencies vào đó
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt


# ----- Stage 2: Runtime (Chạy ứng dụng) -----
FROM python:3.11-slim

WORKDIR /app

# Cài đặt ffmpeg (Runtime cần ffmpeg để chạy)
# LƯU Ý: Nên cài trực tiếp ở đây thay vì copy binary từ stage 1
# vì ffmpeg cần nhiều thư viện liên kết động (.so files), copy tay dễ bị thiếu lỗi.
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# COPY môi trường ảo từ Builder sang Runtime
COPY --from=builder /opt/venv /opt/venv

# COPY code của bạn
COPY . .

# THIẾT LẬP BIẾN MÔI TRƯỜNG QUAN TRỌNG
# Dòng này giúp hệ thống nhận diện được lệnh uvicorn nằm trong /opt/venv/bin
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000

# Chạy app (Lúc này uvicorn đã được tìm thấy nhờ biến PATH ở trên)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]