from fastapi import APIRouter, HTTPException, Depends

from app.api.v1.crud.genre_crud import get_all
from app.core.config import Settings
from app.services import genre_service
from app.schemas.genre_schema import GenreCreateSchema, GenreRequest, GenreUpdateRequest
from app.services.admin_service import get_current_admin
from app.services.genre_service import get_or_create_genre

from app.utils import enum_utils

settings = Settings()

router = APIRouter(prefix=f"{settings.API_VERSION}/genre", tags=["Genre"])

@router.get("/get-all-genres")
def get_all_genres():
    try:
        result = get_all()
        if not result.data:
            raise HTTPException(status_code=404, detail= "User not found in Genres")

        return result

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add-genre")
def add_genre(request: GenreRequest, admin=Depends(get_current_admin)):
    try:
        admin_id = admin["admin_id"]
        admin_role = admin["admin_role"]

        if not enum_utils.check_super_admin(admin_role) and not enum_utils.check_content_manager(admin_role):
            raise HTTPException(status_code=403, detail="You don't have the authority to perform this action")

        genre, code = get_or_create_genre(genre_in = GenreCreateSchema(genre_name = request.genre_name, genre_info = None if request.genre_info == "" else request.info), admin_id=admin_id)

        if code == 2:
            msg = "Add genre successfully"
        elif code == 1:
            msg = "Genre already exists"
        else:
            msg = "Add genre failed"

        return {"message": msg}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update-genre")
def update_genre(request: GenreUpdateRequest, admin = Depends(get_current_admin)):
    try:
        admin_id = admin["admin_id"]
        admin_role = admin["admin_role"]

        if not enum_utils.check_super_admin(admin_role) and not enum_utils.check_content_manager(admin_role):
            raise HTTPException(status_code=403, detail="You don't have the authority to perform this action")

        update = genre_service.update_genre(admin_id=admin_id, genre_id=request.genre_id,
                                   genre_in = GenreCreateSchema(genre_name = request.genre_name, genre_info = request.genre_info))

        if update is None:
            raise HTTPException(status_code=500, detail="Update genre failed")

        return {"message": "Update successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))