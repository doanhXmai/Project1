from typing import List

from app.api.v1.crud import genre_crud
from app.schemas.genre_schema import GenreCreateSchema

from app.utils.log import ConsoleLogger as cl

from app.services.history_update_service import create_history


def get_or_create_genre(admin_id: int, genre_in: GenreCreateSchema):
    try:
        existing = get_genre(genre_in=genre_in)

        if existing:
            return existing, 1

        return create_genre(admin_id, genre_in), 2
    except Exception as e:
        cl.error(f"get or create genre error: {e}")
        return None, 0

def get_genre(genre_in: GenreCreateSchema = None, genre_name: str = None, genre_id: int = None):
    try:
        if genre_in:
            result = genre_crud.get_genre_by_name(genre_in.genre_name)
        elif genre_name:
            result = genre_crud.get_genre_by_name(genre_name)
        elif genre_id:
            result = genre_crud.get_genre_by_id(genre_id)
        else:
            return None

        return result.data[0] if result.data else None

    except Exception as e:
        print("Get genre error: ", e)
        return None

def create_genre(admin_id, genre_in: GenreCreateSchema):
    try:
        new_genre = genre_crud.create_genre(genre_in)

        status, msg = create_history({"genre_id": new_genre.data[0]["genre_id"]}, admin_id, [f"Add a new genre-{genre_in.genre_name}"], True)

        if not status:
            cl.warn(msg)

        return new_genre.data[0] if new_genre.data else None

    except Exception as e:
        cl.error("Create genre error:" + str(e))
        return None

def update_genre(admin_id: int, genre_id: int, genre_in: GenreCreateSchema):
    try:
        if not genre_in or not genre_in:
            return None

        existing = get_genre(genre_id=genre_id)

        if not existing:
            return None

        if genre_in.genre_name == "":
            genre_in.genre_name = existing["genre_name"]

        if genre_in.genre_info == "":
            genre_in.genre_info = existing["genre_info"]

        update = genre_crud.update_genre(genre_id = genre_id, genre = genre_in)

        status, msg = create_history({"genre_id": update.data[0]["genre_id"]}, admin_id, [f"Update a genre-{genre_in.genre_name}"], True)

        if not status:
            cl.warn(msg)

        return update.data[0] if update.data else None

    except Exception as e:
         cl.error (f"Update genre error: {e}")
         return None


def id_to_genre(singer_name: str):
    try:
        result = genre_crud.get_genre_id_by_name(singer_name)
        return result.data[0]
    except Exception as e:
        cl.error(f"id to genre scheme error: {e}")
        return None


def id_to_genres(singer_names: List[str]):
    list_id = []
    for name in singer_names:
        list_id.append(id_to_genre(name)["genre_id"])
    return list_id