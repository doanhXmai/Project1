from app.core.supabase import supabase_py_service_client


def get_all():
    return (supabase_py_service_client.table("Tracks")
            .select("track_id, track_title, track_poster_url, track_duration, track_total_view")
            .execute())

def get_track_banner():
    return (supabase_py_service_client.table("Tracks")
            .select("track_id, track_banner_url, track_total_view")
            .execute())

def get_track_by_name(track_name: str):
    return supabase_py_service_client.table("Tracks").select("*").eq("track_name", track_name).execute()

def get_track_by_id(track_id: int):
    return supabase_py_service_client.table("Tracks").select("*").eq("track_id", track_id).execute()

def create_track_by_admin():
