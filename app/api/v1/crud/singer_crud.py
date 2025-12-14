from app.core.supabase import supabase_py_service_client
from app.schemas.singer_schema import SingerCreateSchema


def get_all():
    return supabase_py_service_client.table("Singers").select("*").execute()

def get_singer_id_by_name(name: str):
    return supabase_py_service_client.table("Singers").select("singer_id").eq("singer_name", name).execute()

def get_singer_by_id(singer_id: int):
    return supabase_py_service_client.table("Singers").select("*").eq("singer_id", singer_id).execute()

def get_singer_by_name(singer_name: str):
    return supabase_py_service_client.table("Singers").select("*").eq("singer_name", singer_name).execute()

def get_all_info_singer(singer_id):
    return supabase_py_service_client.table("Singers").select(
        """*, 
        OfficialAlbums(*),
        Track_Singer (
            Tracks(track_id,track_title, track_info,track_duration, track_lyric_url, track_poster_url, track_banner_url,track_audio_url, track_officialAlbum_id,track_upload_date,track_total_view)
        )"""
    ).eq("singer_id", singer_id).execute()

def create_singer(singer: SingerCreateSchema):
    return supabase_py_service_client.table("Singers").insert({
        "singer_name": singer.singer_name,
        "singer_info": singer.singer_info,
        "singer_view": 0
    }).execute()

def update_singer(singer_id, singer: SingerCreateSchema):
    return supabase_py_service_client.table("Singers").update({
        "singer_name": singer.singer_name,
        "singer_info": singer.singer_info,
        "singer_view": singer.singer_view
    }).eq("singer_id", singer_id).execute()