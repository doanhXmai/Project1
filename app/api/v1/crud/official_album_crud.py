from app.core.supabase import supabase_py_service_client
from app.schemas.official_album_schema import OfficialAlbumSchema, OfficialAlbumUpdateSchema

OFFICIAL_ALBUM_FIELDS = ("officialAlbum_id, officialAlbum_singer_id, "
            "officialAlbum_name, officialAlbum_info, "
            "officialAlbum_release_date, officialAlbum_uploader_admin_id, "
            "officialAlbum_target_type")

def get_official_albums():
    return (supabase_py_service_client
            .table("OfficialAlbums")
            .select(OFFICIAL_ALBUM_FIELDS)
            .execute())

def get_official_album_by_id(oa_id: int):
    return (supabase_py_service_client
            .table("OfficialAlbums")
            .select(OFFICIAL_ALBUM_FIELDS)
            .eq("officialAlbum_id", oa_id)
            .execute())

def get_official_album_by_singer_id(singer_id: int):
    return (supabase_py_service_client
            .table("OfficialAlbums")
            .select(OFFICIAL_ALBUM_FIELDS)
            .eq("officialAlbum_singer_id", singer_id)
            .execute())

def get_official_album_by_name(oa_name: str):
    return (supabase_py_service_client
            .table("OfficialAlbums")
            .select(OFFICIAL_ALBUM_FIELDS)
            .eq("officialAlbum_name", oa_name)
            .execute())

def get_official_album_by_admin_id(admin_id: int):
    return (supabase_py_service_client
            .table("OfficialAlbums")
            .select(OFFICIAL_ALBUM_FIELDS)
            .eq("officialAlbum_uploader_admin_id", admin_id)
            .execute())

def create_official_album_by_admin_id(oa: OfficialAlbumSchema, admin_id: int):
    return supabase_py_service_client.table("OfficialAlbums").insert({
        "officialAlbum_singer_id": oa.officialAlbum_singer_id,
        "officialAlbum_name": oa.officialAlbum_name,
        "officialAlbum_info": oa.officialAlbum_info,
        "officialAlbum_release_date": oa.officialAlbum_release_date,
        "officialAlbum_uploader_admin_id": admin_id,
        "officialAlbum_uploader_user_id": None,
        "officialAlbum_target_type": oa.officialAlbum_target_type
    }).execute()

def update_official_album_by_id(oa: OfficialAlbumUpdateSchema, oa_id):
    return supabase_py_service_client.table("OfficialAlbums").update({
        "officialAlbum_singer_id": oa.officialAlbum_singer_id,
        "officialAlbum_name": oa.officialAlbum_name,
        "officialAlbum_info": oa.officialAlbum_info,
        "officialAlbum_release_date": oa.officialAlbum_release_date
    }).eq("officialAlbum_id", oa_id).execute()

def update_official_album_by_name(oa: OfficialAlbumSchema, oa_name):
    return supabase_py_service_client.table("OfficialAlbums").update({
        "officialAlbum_singer_id": oa.officialAlbum_singer_id,
        "officialAlbum_name": oa.officialAlbum_name,
        "officialAlbum_info": oa.officialAlbum_info,
        "officialAlbum_release_date": oa.officialAlbum_release_date
    }).eq("officialAlbum_name", oa_name).execute()