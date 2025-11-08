# API Documentation

## Authentication
| i | Method | Endpoint                                 | Description                                           |
|---|--------|------------------------------------------|-------------------------------------------------------|
| 1 | POST   | `/api/v1/auth/register-by-email`         | Đăng ký tài khoản với email                           |
| 2 | POST   | `/api/v1/auth/login-by-email`            | Đăng nhập tài khoản với email                         |
| 3 | POST   | `/api/v1/auth/refresh-access-token`      | Tạo mới access_token mỗi lần gửi request              |
| 4 | POST   | `/api/v1/auth/forgot-password-by-email`  | Sử dụng email để đổi mật khẩu khi quên mật khẩu       |
| 5 | POST   | `/api/v1/auth/reset-password`            | Sử dụng access_token tạm được gửi về để đổi mật khẩu  |
| 6 | POST   | `/api/v1/auth/change-password-by-email`  | Sử dụng email để đổi mật khẩu khi đã đăng nhập        |

## Users

## Admins

## Home
| i | Method | Endpoint                      | Description                                     |
|---|--------|-------------------------------|-------------------------------------------------|
| 1 | GET    | `/api/v1/home/get-all-tracks` | Trả về 1 danh sách các bài hát có trên nền tảng |
| 2 | GET    | `/api/v1/home/get-tracks`     | Trả về 1 bài hát theo tiêu chí xác định         |