from app.core.supabase import supabase_py
from app.schemas.official_album_schema import OfficialAlbumCreateSchema, OfficialResponseSchema
from app.schemas.singer_schema import SingerResponseSchema


def get_official_album(album: OfficialAlbumCreateSchema = None, album_name: str = None, album_id: int = None):
    try:
        query = supabase_py.table("OfficialAlbums").select("*, Singers(*)")
        if album:
            query = query.eq("officialAlbum_name", album.officialAlbum_name)
        elif album_name:
            query = query.eq("officialAlbum_name", album_name)
        elif album_id:
            query = query.eq("officialAlbum_id", album_id)
        else:
            return None

        result = query.single().execute()

        row = result.data
        if not row:
            return None

        return OfficialResponseSchema(
            officialAlbum_id = row["officialAlbum_id"],
            officialAlbum_uploader_user_id = row["officialAlbum_uploader_user_id"],
            singer = SingerResponseSchema(**row["Singers"]),
            officialAlbum_name = row["officialAlbum_name"],
            officialAlbum_release_date = row["officialAlbum_release_date"],
            officialAlbum_info = row["officialAlbum_info"]
        )
    except Exception as e:
        print("Get official album error: ", e)
        return None