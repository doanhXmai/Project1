from fastapi import APIRouter, HTTPException

from app.core.config import Settings
from app.core.supabase import supabase_py
from app.schemas.genre_schema import GenreCreateSchema, GenreRequest
from app.services.genre_service import get_or_create_genre

settings = Settings()

router = APIRouter(prefix=f"{settings.API_VERSION}/genre", tags=["Genre"])

@router.get("/get-all-genres")
def get_all_genres():
    try:
        result = supabase_py.table("Genres").select("*").execute()
        if not result.data:
            raise HTTPException(status_code=404, detail= "User not found in Genres")
        return result
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add-genre")
def add_genre(request: GenreRequest):
    try:
        get_or_create_genre(genre_in = GenreCreateSchema(genre_name = request.name, genre_info = request.info))
        return {"message": "Add genre successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

