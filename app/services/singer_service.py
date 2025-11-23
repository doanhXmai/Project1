from app.core.supabase import supabase_py, supabase_py_service_client
from app.schemas.singer_schema import SingerCreateSchema, SingerResponseSchema


def get_or_create_singer(singer_in: SingerCreateSchema):
    try:
        result = supabase_py.table("Singers").select("*").eq("singer_name", singer_in.name).execute()
        if result.data:
            existing = result.data[0]
            return SingerResponseSchema(
                id=existing["singer_id"],
                name=existing["singer_name"],
                info=existing["singer_info"]
            )

        new_singer = supabase_py_service_client.table("Singers").insert({
            "singer_name": singer_in.name,
            "singer_info": singer_in.info
        }).execute()
        created = new_singer.data[0]
        return SingerResponseSchema(
            id=created["singer_id"],
            name=created["singer_name"],
            info=created["singer_info"]
        )
    except Exception as e:
        print("Get or create singer error: ", e)
        return None

def get_singer_by_name(singer_name: str):
    try:
        result = supabase_py.table("Singers").select("*").eq("Singer_name", singer_name).execute()
        existing = result.data[0]
        return SingerResponseSchema(
            id=existing["singer_id"],
            name=existing["singer_name"],
            info=existing["singer_info"]
        )
    except Exception as e:
        print("Singer by name error: ", e)
        return None

def get_singer_by_id(singer_id: int):
    try:
        result = supabase_py.table("Singers").select("*").eq("singer_id", singer_id).execute()
        existing = result.data[0]
        return SingerResponseSchema(
            id=existing["singer_id"],
            name=existing["singer_name"],
            info=existing["singer_info"]
        )
    except Exception as e:
        print("Singer by id error: ", e)
        return None