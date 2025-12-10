from fastapi import APIRouter, HTTPException

from app.core.config import Settings
from app.core.supabase import supabase_py
from app.schemas.home_schema import GetTrackRequest

settings = Settings()

router = APIRouter(prefix=f"{settings.API_VERSION}/home", tags=["Home"])

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
