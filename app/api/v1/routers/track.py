from fastapi import APIRouter, Form, UploadFile, File, Depends, HTTPException

from app.core.config import Settings
from app.core.supabase import supabase_py_service_client, supabase_py
from app.schemas.genre_schema import id_to_genre_schema, GenreResponseSchema, GenreCreateSchema
from app.schemas.home_schema import GetTrackRequest
from app.schemas.singer_schema import id_to_singer_schema, SingerCreateSchema, SingerResponseSchema
from app.schemas.track_schema import TrackResponseSchema, TrackCreateSchema
from app.services.genre_service import get_or_create_genre
from app.services.official_album_service import get_official_album
from app.services.singer_service import get_or_create_singer
from app.services.admin_service import get_current_admin
from app.utils.storage_utils import upload_to_storage

settings = Settings()

router = APIRouter(prefix = f"{settings.API_VERSION}/track", tags = ["Track"])

@router.get("/get-all-tracks")
def get_all_tracks():
    try:
        all_tracks = supabase_py.table("Tracks").select("*").execute()
        if not all_tracks.data:
            return {"status": "success", "message": "The Data is not available!"}
        return {"status": "success", "data": all_tracks.data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/get-tracks")
def get_tracks(request: GetTrackRequest):
    try:
        result = supabase_py.table("Tracks").select("*").like("track_title", request.name).execute()
        if not result.data:
            return {"status": "success", "message": "Track not found!"}
        return {"status": "success", "message": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-banner")
def get_banners():


@router.post("/add-track", response_model=TrackResponseSchema)
async def add_track(data: str = Form(...),
                    track_poster: UploadFile = File(None),
                    track_audio: UploadFile = File(...),
                    track_banner: UploadFile = File(...),
                    admin = Depends(get_current_admin)
                    ):
    try:
        track_data = TrackCreateSchema.model_validate_json(data)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid track data: {str(e)}")
    try:
        admin_id = admin["id"]
        poster_url = None
        if track_poster:
            poster_url = await upload_to_storage(
                settings.DEFAULT_IMAGE_BUCKET,
                f"posters/{track_data.title}_{admin_id}.jpg",
                track_poster
            )

        audio_url = None
        if track_audio:
            audio_url = await upload_to_storage(
                settings.DEFAULT_AUDIO_BUCKET,
                f"audios/{track_data.title}_{admin_id}.mp3",
                track_audio
            )

        insert_data = {
            "track_uploader_user_id": admin_id,
            "track_title": track_data.title,
            "track_info": track_data.info,
            "track_duration": track_data.duration,
            "track_poster_url": poster_url,
            "track_audio_url": audio_url,
            "track_officialAlbum_id": track_data.official_album_id
        }
        created = supabase_py_service_client.table("Tracks").insert(insert_data).execute()
        track_id = created.data[0]["track_id"]

        singer_items = []
        for s in track_data.singers:
            singer_response: SingerResponseSchema = get_or_create_singer(SingerCreateSchema(name=s))
            singer_id = singer_response.id
            supabase_py_service_client.table("Track_Singer").insert({
                "track_id": track_id,
                "singer_id": singer_id
            }).execute()
            singer_items.append(singer_id)

        genre_items = []
        for g in track_data.genres:
            genre_response: GenreResponseSchema = get_or_create_genre(GenreCreateSchema(name=g))
            genre_id = genre_response.id
            supabase_py_service_client.table("Track_Genre").insert({
                "track_id": track_id,
                "genre_id": genre_id
            }).execute()
            genre_items.append(genre_id)

        track_record = supabase_py_service_client.table("Tracks").select("*").eq("track_id", track_id).single().execute().data

        response = TrackResponseSchema(
            id = track_record["track_id"],
            title = track_record["track_title"],
            info = track_record["track_info"],
            duration = track_record["track_duration"],
            poster_url = track_record["track_poster_url"],
            audio_url = track_record["track_audio_url"],
            user_id = track_record["track_uploader_user_id"],
            official_album = get_official_album(track_data.official_album_id),
            singers = [id_to_singer_schema(sid) for sid in singer_items],
            genres = [id_to_genre_schema(gid) for gid in genre_items]
        )

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))