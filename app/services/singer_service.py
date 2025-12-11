from app.api.v1.crud.genre_crud import create_genre
from app.core.supabase import supabase_py, supabase_py_service_client
from app.schemas.singer_schema import SingerCreateSchema, SingerResponseSchema
from app.api.v1.crud import singer_crud
from app.services.history_update_service import create_history
from app.utils.log import ConsoleLogger as cl

def get_or_create_singer(singer_in: SingerCreateSchema, admin_id: int):
    try:
        existing = get_singer(singer_in = singer_in)

        if existing:
            return existing, 1

        return create_singer(singer_in = singer_in, admin_id = admin_id), 2
    except Exception as e:
        cl.error(f"Get or create singer error: {e}")
        return None

def get_singer(singer_in: SingerCreateSchema = None, singer_name: str = None, singer_id: int = None):
    try:
        if singer_in:
            result = singer_crud.get_singer_by_name(singer_in.singer_name)
        elif singer_name:
            result = singer_crud.get_singer_by_name(singer_name)
        elif singer_id:
            result = singer_crud.get_singer_by_id(singer_id)
        else:
            return None

        return result.data[0] if result.data else None

    except Exception as e:
        cl.error(f"Get singer error: {e}")

def create_singer(singer_in: SingerCreateSchema, admin_id: int):
    try:
        if not singer_in.singer_view:
            singer_in.singer_view = 0

        new_singer = singer_crud.create_singer(singer_in)

        status, msg = create_history({"singer_id": new_singer.data[0]["singer_id"]}, admin_id, [f"Add a new singer-{singer_in.singer_name}"], True)

        if not status:
            cl.warn(msg)

        return new_singer.data[0] if new_singer.data else None

    except Exception as e:
        cl.error(f"Create singer error: {e}")
        return None

def update_singer(admin_id: int, singer_id: int, singer_in: SingerCreateSchema):
    try:
        if not singer_in or not singer_id:
            return None

        if not singer_in.singer_view:
            singer_in.singer_view = 0

        existing = get_singer(singer_id=singer_id)

        if not existing:
            cl.warn("Crack o day")
            return None

        if singer_in.singer_name == "":
            singer_in.singer_name = existing["singer_name"]

        if singer_in.singer_info == "":
            singer_in.singer_info = existing["singer_info"]

        update = singer_crud.update_singer(singer_id = singer_id, singer = singer_in)

        status, msg = create_history({"singer_id": update.data[0]["singer_id"]}, admin_id, [f"Update a singer-{singer_in.singer_name}"], True)

        if not status:
            cl.warn(msg)

        return update.data[0] if update.data else None

    except Exception as e:
        cl.error(f"Update singer error: {e}")