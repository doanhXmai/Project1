from fastapi import APIRouter, HTTPException, Depends

from app.core.config import Settings

from app.api.v1.crud import official_album_crud
from app.schemas.official_album_schema import OfficialAlbumSchema, OfficialAlbumUpdateSchema
from app.services.admin_service import get_current_admin
from app.services.history_update_service import create_history

settings = Settings()

router = APIRouter(prefix=f"{settings.API_VERSION}/official-album", tags=["OfficialAlbum"])

@router.get("/get-all")
def get_all():
    try:
        result = official_album_crud.get_official_albums()
        if not result.data:
            raise HTTPException(status_code=404, detail="Official album not found")

        return {
            "number": len(result.data),
            "data": result.data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get official album error: {e}")

@router.get("/get-by-singer/{singer_id}")
def get_by_singer(singer_id):
    try:
        result = official_album_crud.get_official_album_by_singer_id(singer_id)

        if not result.data:
            raise HTTPException(status_code=404, detail=f"Official album of {singer_id} not found")

        return {
            "number": len(result.data),
            "data": result.data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get official album by {singer_id} error: {e}")


@router.get("/get-by-admin/{admin_id}")
def get_by_admin(admin_id):
    try:
        result = official_album_crud.get_official_album_by_admin_id(admin_id)

        if not result.data:
            raise HTTPException(status_code=404, detail=f"Official album of {admin_id} not found")

        return {
            "number": len(result.data),
            "data": result.data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get official album by {admin_id} error: {e}")


@router.get("/get-by-name/{name}")
def get_by_name(name):
    try:
        result = official_album_crud.get_official_album_by_name(name)

        if not result.data:
            raise HTTPException(status_code=404, detail=f"Official album - {name} not found")

        return {
            "number": len(result.data),
            "data": result.data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get official album by name - {name} error: {e}")

@router.get("/get-by-id/{official_album_id}")
def get_by_id(official_album_id):
    try:
        result = official_album_crud.get_official_album_by_id(official_album_id)

        if not result.data:
            raise HTTPException(status_code=404, detail=f"Official album - {official_album_id} not found")

        return {
            "number": len(result.data),
            "data": result.data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get official album by id - {official_album_id} error: {e}")

@router.post("/add-official-album")
def add_official_album(request: OfficialAlbumSchema, admin = Depends(get_current_admin)):
    try:
        admin_id= admin["admin_id"]

        result = official_album_crud.create_official_album_by_admin_id(request, admin_id)

        if not result.data:
            raise HTTPException(status_code=400, detail="Create official album failed")

        status, msg = create_history({"official_album_id": result.data[0]["officialAlbum_id"]},
                                     admin_id, [f"Add a new official album - {request.officialAlbum_name}"],
                                     True)

        if not status:
            return {
                "message": "Create official album successfully",
                "success": True,
                "warn": msg
            }

        return {"message": "Create official album successfully", "success": True}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Create official album error: {e}")

@router.patch("/update-official-album-by-id/{official_album_id}")
def update_official_album_by_id(official_album_id: int, request: OfficialAlbumUpdateSchema):
    try:
        existing = official_album_crud.get_official_album_by_id(official_album_id)

        if not existing.data:
            raise HTTPException(status_code=404, detail=f"Official Album with {official_album_id} not exists")

        update = official_album_crud.update_official_album_by_id(request, official_album_id)

        if not update.data:
            raise HTTPException(status_code=400, detail=f"Official Album with {official_album_id} update failed")

        return {
            "message": f"Update official album with {official_album_id} successfully",
            "success": True
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update official album error: {e}")