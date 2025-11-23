from app.enums.enums import AdminRoleEnum


def change_role_enum(role_str: str) -> AdminRoleEnum:
    for role in AdminRoleEnum:
        print (role.value)
        if role.value == role_str:
            return role