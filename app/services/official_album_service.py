from app.core.supabase import supabase_py, supabase_py_service_client
from app.schemas.official_album_schema import OfficialAlbumCreateSchema, OfficialResponseSchema
from app.schemas.singer_schema import id_to_singer_schema


def get_official_album(a_id: int):
    try:
        res = supabase_py.table("OfficialAlbums").select("*").eq("officialAlbum_id", a_id).single().execute()
        row = res.data

        return OfficialResponseSchema(
            id=row["officialAlbum_id"],
            name=row["officialAlbum_name"],
            info=row["officialAlbum_info"],
            release_date=row["officialAlbum_release_date"],
            singer=id_to_singer_schema(row["officialAlbum_singer_id"])  # convert bằng ID
        )
    except Exception as e:
        print("Official Album error: ", e)
        return None

def create_official_album(album_in: OfficialAlbumCreateSchema, singer_id: int = None):
    try:
        result = supabase_py.table("OfficialAlbums").select("*").eq("officialAlbum_name", album_in.name).execute()
        if result.data:
            existing = result.data[0]
            return [
                False,
                OfficialResponseSchema(
                    id=existing["officialAlbum_id"],
                    name=existing["officialAlbum_name"],
                    info=existing["officialAlbum_info"],
                    release_date=existing["officialAlbum_release_date"],
                    singer=id_to_singer_schema(existing["officialAlbum_singer_id"])
                )
            ]

        new_album = supabase_py_service_client.table("OfficialAlbums").insert({
            "officialAlbum_name": album_in.name,
            "officialAlbum_info": album_in.info,
            "officialAlbum_release_date": album_in.release_date,
            "officialAlbum_singer_id": singer_id
        }).execute()

        new = new_album.data[0]

        return [
            True,
            OfficialResponseSchema(
                id=new["officialAlbum_id"],
                name=new["officialAlbum_name"],
                info=new["officialAlbum_info"],
                release_date=new["officialAlbum_release_date"],
                singer=id_to_singer_schema(new["officialAlbum_singer_id"])
            )
        ]

    except Exception as e:
        print("Create album error:", e)
        return [False, None]
