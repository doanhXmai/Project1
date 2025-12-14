import json
import os
import tempfile
from shlex import quote

from fastapi import APIRouter, Form, UploadFile, File, Depends, HTTPException, Query
from typing import List, Optional

from pydantic import ValidationError
from sqlalchemy.testing.plugin.plugin_base import config

from app.services.track_service import resolve_bucket_and_path, make_filename, flatten_detail_track
from app.utils.log import ConsoleLogger as cl
from app.core.config import Settings
from app.core.supabase import supabase_py_service_client
from app.schemas.home_schema import GetTrackRequest
from app.schemas.track_schema import TrackRequestCreateSchema
from app.services.admin_service import get_current_admin
from app.utils.storage_utils import upload_to_storage
from app.utils.track_utils import get_duration
from app.utils import enum_utils
from app.api.v1.crud import track_crud

settings = Settings()

router = APIRouter(prefix = f"{settings.API_VERSION}/track", tags = ["Track"])

@router.get("/get-all-tracks")
def get_all_tracks():
    try:
        all_tracks = track_crud.get_all()
        if not all_tracks.data:
            return {"status": True, "message": "The Data is not available!"}
        return all_tracks.data
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/search")
def search_tracks(
        q: str = Query(..., min_length=1),
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=50)
):
    result = supabase_py_service_client.rpc(
        "search_tracks",
        {
            "keyword": q,
            "page": page,
            "page_size": page_size
        }
    ).execute()

    cl.info(f"query: {q}")
    cl.info(f"page: {page}")
    cl.info(f"page_size: {page_size}")
    cl.info(f"number: {len(result.data)}")

    return result.data


@router.get("/get-banners")
def get_banners():
    try:
        result = track_crud.get_track_banner()
        if not result.data:
            raise HTTPException(status_code=404, detail="Track banner not found")
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get banners error: {e}")


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

@router.get("/get-top-tracks/{limit}")
def get_top_track(limit: int = 10):
    try:
        result = track_crud.get_top_tracks(limit)

        if not result.data:
            raise HTTPException(status_code=404, detail="Tracks not found")

        return result.data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get top track error: {e}")

@router.get("/get-track/{track_id}")
def get_track_by_id(track_id: int):
    try:
        result = track_crud.get_track_detail_by_id(track_id)

        if not result.data:
            raise HTTPException(status_code=404, detail="Track not found")
        else:
            data = flatten_detail_track(result.data)

        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get track by id = {track_id} error: {e}")