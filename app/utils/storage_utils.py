from fastapi import UploadFile

from app.core.config import Settings
from app.core.supabase import supabase_py_service_client, SUPABASE_URL

settings = Settings()

async def upload_to_storage(bucket: str, file_path: str, file: UploadFile):
    file_bytes = await file.read()

    try:
        existing = supabase_py_service_client.storage.from_(bucket).list(
            path = file_path.rsplit("/", 1)[0] if "/" in file_path else ""
        )
        if any(obj["name"] == file_path.split("/")[-1] for obj in existing):
            supabase_py_service_client.storage.from_(bucket).remove([file_path])

        supabase_py_service_client.storage.from_(bucket).upload(
            file_path, file_bytes, {"content-type": file.content_type}
        )
        return f"{SUPABASE_URL}{settings.STORAGE_PUBLIC_PATH}/{bucket}/{file_path}"
    except Exception as e:
        print("Upload error: ", e)
        return None


