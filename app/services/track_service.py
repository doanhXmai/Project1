from fastapi import UploadFile

from app.core.config import Settings

settings = Settings()

def resolve_bucket_and_path(key_in: str, file_name: str):
    if key_in == "track_audio":
        bk = settings.AUDIO_BUCKET
        folder = ""
    elif key_in == "track_banner":
        bk = settings.IMAGE_BUCKET
        folder = "banners"
    elif key_in == "track_poster":
        bk = settings.IMAGE_BUCKET
        folder = "posters"
    else:
        bk = settings.LYRIC_BUCKET
        folder = ""
    p = f"{folder}/{file_name}" if folder else file_name
    return bk, p

def make_filename(file_in: UploadFile, suffix: str, base_name: str):
    if file_in:
        ext = file_in.filename.split(".")[-1]
        return f"{base_name}_{suffix}.{ext}"
    return None

def flatten_detail_track(data):
    if "track_singer" in data:
        data["track_singer"] = [
            item["singers"]
            for item in data["track_singer"]
            if item.get("singers")
        ]

    if "track_genre" in data:
        data["track_genre"] = [
            item["genres"]
            for item in data["track_genre"]
            if item.get("genres")
        ]

    return data