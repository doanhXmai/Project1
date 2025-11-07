from fastapi import APIRouter, HTTPException

from .home_helper import GetTrackRequest
from app.db.supabase_py import supabase_py

router = APIRouter(prefix="/home", tags=["Home"])

@router.get("/get-all-tracks")
def get_all_tracks():
    try:
        all_tracks = supabase_py.table("Tracks").select("*").execute()
        if not all_tracks.data:
            return {"status": "success", "message": "The Data is not available!"}
        return {"status": "success", "data": all_tracks.data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/get-track")
def get_track(request: GetTrackRequest):
    try:
        result = supabase_py.table("Tracks").select("*").like("track_title", GetTrackRequest.name).execute()
        if not result.data:
            return {"status": "success", "message": "Track not found!"}
        return {"status": "success", "message": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
