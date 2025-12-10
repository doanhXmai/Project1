from app.api.v1.crud.admin_crud import check_admin
from app.api.v1.crud.user_crud import check_user
from app.core.config import Settings
from app.core.supabase import supabase_py_service_client

settings = Settings()

def create_history(list_id: dict, target_id, describe: list, is_admin: bool):
    if not list_id:
        return False, {"msg": "List ID is empty"}

    if not describe or len(describe) != len(list_id):
        return False, {"msg": "Describe list must match list_id length"}

    if is_admin:
        if not check_admin(admin_id=target_id):
            return False, {"msg": f"Admin ID not found: {target_id}"}

    else:
        if not check_user(user_id=target_id):
            return False, {"msg": f"User ID not found: {target_id}"}

    try:
        records = []

        now = settings.DATE_NOW.isoformat()

        for idx, (key, value) in enumerate(list_id.items()):
            insert_data = {
                "historyUpdate_date": now,
                "historyUpdate_target_type": is_admin,
                "historyUpdate_admin_id": target_id if is_admin else None,
                "historyUpdate_user_id": target_id if not is_admin else None,
                "historyUpdate_description": describe[idx],
                f"historyUpdate_{key}": value
            }
            records.append(insert_data)

        # Insert nhiều record một lúc
        supabase_py_service_client.table("HistoryUpdate").insert(records).execute()

        return True, {"msg": f"Created {len(records)} records successfully"}

    except Exception as e:
        return False, {"msg": f"create history error: {e}"}