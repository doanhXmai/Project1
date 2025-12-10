from app.enums.enums import AdminRoleEnum


def change_role_enum(role_str: str) -> AdminRoleEnum:
    for role in AdminRoleEnum:
        print (role.value)
        if role.value == role_str:
            return role

def check_super_admin(role_str: str) -> bool:
    role = change_role_enum(role_str)

    if AdminRoleEnum.SUPER_ADMIN != role:
        return False

    return True


def check_admin(role_str: str) -> bool:
    role = change_role_enum(role_str)

    if AdminRoleEnum.ADMIN != role:
        return False

    return True


def check_content_manager(role_str: str) -> bool:
    role = change_role_enum(role_str)

    if AdminRoleEnum.CONTENT_MANAGER != role:
        return False

    return True


def check_moderator(role_str: str) -> bool:
    role = change_role_enum(role_str)

    if AdminRoleEnum.MODERATOR != role:
        return False

    return True


def check_support_staff(role_str: str) -> bool:
    role = change_role_enum(role_str)

    if AdminRoleEnum.SUPPORT_STAFF != role:
        return False

    return True