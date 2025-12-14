from app.core.supabase import supabase_py_service_client

def get_all():
    return (supabase_py_service_client.table("Tracks")
            .select("track_id,track_title,"
                    "track_info, track_duration,"
                    "track_lyric_url, track_poster_url,"
                    "track_banner_url, track_audio_url,"
                    "track_officialAlbum_id, track_upload_date, track_total_view")
            .execute())

def get_track_banner():
    return (supabase_py_service_client.table("Tracks")
            .select("track_id, track_title, track_banner_url, track_total_view")
            .execute())

def get_track_by_name(track_name: str):
    return supabase_py_service_client.table("Tracks").select("*").eq("track_name", track_name).execute()

def get_track_by_id(track_id: int):
    return supabase_py_service_client.table("Tracks").select("*").eq("track_id", track_id).execute()

def get_top_tracks(limit: int = 10):
    return (supabase_py_service_client
            .table("Tracks").select("track_id, track_title, track_poster_url, track_audio_url, track_duration, track_total_view")
            .order("track_total_view", desc=True)
            .limit(limit)
            .execute()
    )

def get_track_detail_by_id(track_id):
    return supabase_py_service_client.table("Tracks").select(
        """
        track_id,track_title, 
        track_info,track_duration, track_lyric_url,
        track_poster_url, track_banner_url,
        track_audio_url, track_upload_date,track_total_view, 
        official_album: OfficialAlbums(
            officialAlbum_id,
            officialAlbum_name
        ),
        track_singer: Track_Singer(
            singers: Singers (
                singer_id,
                singer_name
            )
        ),
        track_genre: Track_Genre (
            genres: Genres (
                genre_id,
                genre_name
            )
        )
        """
    ).eq("track_id", track_id).single().execute()

# def create_track_by_admin():
#     return supabase_py_service_client.table("Tracks").insert({
#
#     })