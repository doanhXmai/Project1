| lv | role            | Ý nghĩa                                                                                                                                                 |
|----|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| 5  | super_admin     | Có tất cả các quyền của các quyền admin khác(dùng để tạo các tài khoản admin)                                                                           |
| 4  | admin           | Có quyền quản lý tài khoản(thêm/sửa/xoá/vô hiệu hoá) tài khoản admin ngoại trừ super_admin và admin. Quản lý tài khoản người dùng (sửa/xoá/vô hiệu hoá) |
| 3  | content_manager | Có quyền sửa xoá bài hát, album, official album, thể loại                                                                                               |
| 2  | moderator       | Kiểm duyệt nội dung bị report, khoá bài hát/playlist bị tố cáo chỉ phê duyệt và từ chối(approve/reject) - không được sửa/xoá                            |
| 1  | support staff   | Chỉ được đọc thông tin của user(read-only), Gửi yêu cầu kháo tài khoản hoặc reset mật khẩu                                                              |
