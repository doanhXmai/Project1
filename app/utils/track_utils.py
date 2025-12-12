import os
import subprocess
import json
import tempfile
from datetime import timedelta

from fastapi import UploadFile

from app.utils.log import ConsoleLogger as cl

def get_audio_duration(file_path: str) -> float:
    cmd = [
        "ffprobe",
        "-v", "error",     # Hiện lỗi rõ ràng
        "-print_format", "json",
        "-show_entries", "format=duration",
        file_path
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout = result.stdout.decode()
    stderr = result.stderr.decode()

    cl.info(f"FFPROBE STDOUT: {stdout}")
    cl.info(f"FFPROBE STDERR: {stderr}")

    if not stdout.strip():
        return -1.0

    try:
        data = json.loads(stdout)
        return float(data["format"]["duration"])
    except Exception as e:
        cl.error(f"JSON parse error: {e}")
        return -1.0

def seconds_to_time_format(seconds: float) -> str:
    td = timedelta(seconds=round(seconds))
    return str(td)

async def get_duration(upload_file):
    # Lấy đuôi file
    suffix = os.path.splitext(upload_file.filename)[1]

    # Tạo file tạm
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
        content = await upload_file.read()      # Đọc file 1 lần
        temp.write(content)
        temp.flush()
        temp_path = temp.name

    # Reset file pointer để upload không bị rỗng
    upload_file.file.seek(0)

    # Tính duration
    duration_seconds = get_audio_duration(temp_path)

    # Xóa file tạm
    os.remove(temp_path)

    # Xử lý lỗi
    if duration_seconds == -1.0:
        return 0, 0

    # Chuyển sang dạng hh:mm:ss
    duration_time = seconds_to_time_format(duration_seconds)

    return duration_seconds, duration_time