from fastapi import APIRouter, HTTPException, Depends

from app.api.v1.crud import singer_crud
from app.api.v1.crud.singer_crud import get_all
from app.core.config import Settings
from app.schemas.singer_schema import SingerCreateSchema, SingerRequest, SingerUpdateRequest
from app.services.admin_service import get_current_admin
from app.services import singer_service
from app.utils import enum_utils
from app.utils.log import ConsoleLogger as cl

settings = Settings()

router = APIRouter(prefix=f"{settings.API_VERSION}/singer", tags=["Singer"])

@router.get("/get-all-singers")
def get_all_singers():
    try:
        result = get_all()
        if not result.data:
            raise HTTPException(status_code=404, detail="User not found in Singers")

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-singer/{singer_id}")
def get_singer_by_id(singer_id: int):
    try:
        result = singer_crud.get_all_info_singer(singer_id)
        if not result.data:
            raise HTTPException(status_code=404, detail="Singer not found")
        return result.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get all info singer by id error: {e}")
@router.post("/add-singer")
def add_singer(request: SingerRequest, admin=Depends(get_current_admin)):
    try:
        admin_id = admin["admin_id"]
        cl.info(f"Day la id cua admin - {admin_id}")
        admin_role = admin["admin_role"]

        if not enum_utils.check_super_admin(admin_role) and not enum_utils.check_content_manager(admin_role):
            raise HTTPException(status_code=403, detail="You don't have the authority to perform this action")

        singer, code = singer_service.get_or_create_singer(singer_in=SingerCreateSchema(singer_name = request.singer_name, singer_info = None if request.singer_info == "" else request.singer_info),
                                                                                        admin_id = admin_id)

        if code == 2:
            msg = "Add singer successfully"
        elif code == 1:
            msg = "Singer already exists"
        else:
            msg = "Add singer failed"

        return {"message": msg}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update-singer")
def update_singer(request: SingerUpdateRequest, admin = Depends(get_current_admin)):
    try:
        admin_id = admin["admin_id"]
        admin_role = admin["admin_role"]

        if not enum_utils.check_super_admin(admin_role) and not enum_utils.check_content_manager(admin_role):
            raise HTTPException(status_code=403, detail="You don't have the authority to perform this action")

        update = singer_service.update_singer(admin_id=admin_id, singer_id=request.singer_id,
                                              singer_in=SingerCreateSchema(singer_name=request.singer_name, singer_info=request.singer_info, singer_view = request.singer_view))

        if update is None:
            raise HTTPException(status_code=500, detail="Update singer failed")

        return {"message": "Update successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))