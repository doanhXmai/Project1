from enum import Enum

"""
super_admin: toàn quyền - có thể tạo các tài khoản admin khác
admin:
    (+) quản lý người dùng, nghệ sĩ, bài hát, album
    (+) quản lý thể loại
    (+) có thể tạo các tài khoản admin có quyền thấp hơn (admin)
    (+) quản lý user/admin(trừ super và admin cùng cấp)
content_manager:
    (+) sửa/xoá bài hát, album, official album
    (+) quản lý thể loại, official album
    (-) không có quyền quản lý user/admin
moderator:
    (+) kiểm duyệt nội dung bị report
    (+) khoá bài hát/playlist bị tố cáo
    (-) không sửa được thông tin chỉ approve/reject
support staff:
    (+) Xem thông tin user - chỉ đọc(read-only)
    (+) Gửi yêu cầu khoá tài khoản hoặc reset mật khẩu
"""

class AdminRoleEnum(Enum):
    SUPER_ADMIN = ("supper_admin", 5)
    ADMIN = ("admin", 4)
    CONTENT_MANAGER = ("content_manager", 3)
    MODERATOR = ("moderator", 2)
    SUPPORT_STAFF = ("support_staff", 1)

    def __init__(self, value, level):
        self._value_ = value
        self.level = level

    def __lt__(self, other):
        return self.level < other.level
    def __le__(self, other):
        return self.level <= other.level

    def __gt__(self, other):
        return self.level > other.level
    def __ge__(self, other):
        return self.level >= other.level
