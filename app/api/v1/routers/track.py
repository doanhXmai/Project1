import json
import os
import tempfile
from shlex import quote

from fastapi import APIRouter, Form, UploadFile, File, Depends, HTTPException
from typing import List

from pydantic import ValidationError

from app.services.genre_service import id_to_genres
from app.services.singer_service import id_to_singers
from app.services.track_service import resolve_bucket_and_path, make_filename
from app.utils.log import ConsoleLogger as cl
from app.core.config import Settings
from app.core.supabase import supabase_py_service_client
from app.schemas.home_schema import GetTrackRequest
from app.schemas.track_schema import TrackRequestCreateSchema
from app.services.admin_service import get_current_admin
from app.utils.storage_utils import upload_to_storage
from app.utils.track_utils import get_duration
from app.utils import enum_utils

settings = Settings()

router = APIRouter(prefix = f"{settings.API_VERSION}/track", tags = ["Track"])

@router.get("/get-all-tracks")
def get_all_tracks():
    try:
        all_tracks = supabase_py_service_client.table("Tracks").select("*").execute()
        if not all_tracks.data:
            return {"status": "success", "message": "The Data is not available!"}
        return {"status": "success", "data": all_tracks.data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/get-tracks")
def get_tracks(request: GetTrackRequest):
    try:
        result = supabase_py_service_client.table("Tracks").select("*").like("track_title", request.name).execute()
        if not result.data:
            return {"status": "success", "message": "Track not found!"}
        return {"status": "success", "message": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @router.get("/get-banner")
# def get_banners():


@router.post("/add-track")
async def add_track(data: str = Form(...),
                    track_lyrics: UploadFile = File(None),
                    track_poster: UploadFile = File(None),
                    track_audio: UploadFile = File(...),
                    track_banner: UploadFile = File(...),
                    track_singers: List[str] = Form(...),
                    track_genres: List[str] = Form(...),
                    admin = Depends(get_current_admin)
                    ):
    try:
        track_in = TrackRequestCreateSchema.model_validate_json(data)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON in 'data' field - {e}")

    now = settings.DATE_NOW.isoformat()

    admin_id = admin["admin_id"]
    admin_role = admin["admin_role"]

    if not enum_utils.check_super_admin(admin_role) and not enum_utils.check_content_manager(admin_role):
        raise HTTPException(status_code=403, detail="No permission")

    base_name = f"{track_in.track_title}_{'_'.join(track_singers)}".replace(" ", "_")

    duration_seconds, duration_time = await get_duration(track_audio)

    file_map = [
        ("track_audio", track_audio, make_filename(track_audio, "audio", base_name)),
        ("track_banner", track_banner, make_filename(track_banner, "banner", base_name)),
        ("track_poster", track_poster, make_filename(track_poster, "poster", base_name)),
        ("track_lyrics", track_lyrics, make_filename(track_lyrics, "lyrics", base_name)),
    ]

    uploaded_urls = {}

    for key, file, filename in file_map:
        if file is None:
            uploaded_urls[key] = None
            continue

        bucket, path = resolve_bucket_and_path(key, filename)

        url = await upload_to_storage(bucket, path, file)

        if not url:
            raise HTTPException(status_code=500, detail=f"Upload failed for {filename}")

        uploaded_urls[key] = url

    track_data = {
        "track_title": track_in.track_title,
        "track_info": track_in.track_info,
        "track_duration": duration_time,
        "track_audio_url": uploaded_urls["track_audio"],
        "track_banner_url": uploaded_urls["track_banner"],
        "track_poster_url": uploaded_urls["track_poster"],
        "track_lyric_url": uploaded_urls["track_lyrics"],
        "track_officialAlbum_id": track_in.track_officialAlbum_id,
        "track_upload_date": now,
        "track_total_view": 0,

        "track_uploader_admin_id": admin_id,
        "track_target_type": True
    }

    try:
        insert_res = supabase_py_service_client.table("Tracks").insert(track_data).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Supabase insert error: {str(e)}")

    track_id = insert_res.data[0]["track_id"]

    if len(track_singers) > 0:
        for id_singer in track_singers:
            supabase_py_service_client.table("Track_Singer").insert({
                "track_id": track_id,
                "singer_id": id_singer
            }).execute()

    if len(track_genres) > 0:
        for id_genre in track_genres:
            supabase_py_service_client.table("Track_Genre").insert({
                "track_id": track_id,
                "genre_id": id_genre
            }).execute()

    return {
        "message": "Track created successfully",
        "duration_time": duration_time,
        "files": uploaded_urls
    }