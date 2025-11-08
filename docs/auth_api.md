# Authentication API Documentation
- Tài liệu mô tả chi tiết các API liên quan đến phần xác thực(Auth) người dùng.

---

## 1. Register by email
**Method:** `POST`
**Endpoint:** `/api/v1/auth/register-by-email`
**Description:** Đăng ký tài khoản mới bằng email và mật khẩu

### Request Body
| Filed    | Type    | Required | Description         |
|----------|---------|----------|---------------------|
| email    | string  | ✅        | Email người dùng    |
| password | string  | ✅        | Mật khẩu người dùng |

### Example Request
```json
{
  "email": "user@example.com",
  "password": "abc@123"
}
```

## 2. Login by email
**Method:** `POST`
**Endpoint:** `/api/v1/auth/login-by-email`
**Description:** Đăng nhập tài khoản bằng email và mật khẩu

### Request Body
| Filed    | Type    | Required | Description         |
|----------|---------|----------|---------------------|
| email    | string  | ✅        | Email người dùng    |
| password | string  | ✅        | Mật khẩu người dùng |

### Example Request
```json
{
  "email": "user@example.com",
  "password": "abc@123"
}
```

## 3. Refresh access token by email
**Method:** `POST`
**Endpoint:** `/api/v1/auth/refresh-access-token`
**Description:** Tạo mới access token sau mỗi lần request

### Request Body
| Filed                | Type    | Required | Description                        |
|----------------------|---------|----------|------------------------------------|
| refresh_access_token | string  | ✅        | token dùng để cấp lại access token |

### Example Request
```json
{
  "access_token": "youraccesstoken...."
}
```

## 4. Forgot password by email
**Method:** `POST`
**Endpoint:** `/api/v1/auth/forgot-password-by-email`
**Description:** Lấy lại mật khẩu khi đã quên mật khẩu

### Request Body
| Filed    | Type    | Required | Description         |
|----------|---------|----------|---------------------|
| email    | string  | ✅        | Email người dùng    |

### Example Request
```json
{
  "email": "user@example.com"
}
```

## 5. Reset Password
**Method:** `POST`
**Endpoint:** `/api/v1/auth/reset-password`
**Description:** Thay đổi mật khẩu

### Request Body
| Filed        | Type    | Required | Description         |
|--------------|---------|----------|---------------------|
| password     | string  | ✅        | Mật khẩu người dùng |
| access_token | string  | ✅        | access token tạm    |

### Example Request
```json
{
  "access_token": "youraccesstoken....",
  "password": "abc@123"
}
```
## 6. Change password by email
**Method:** `POST`
**Endpoint:** `/api/v1/auth/change-password-by-email`
**Description:** Thay đổi mật khẩu bằng email và mật khẩu cũ

### Request Body
| Filed        | Type    | Required | Description             |
|--------------|---------|----------|-------------------------|
| email        | string  | ✅        | access token tạm        |
| old_password | string  | ✅        | Mật khẩu cũ người dùng  |
| new_password | string  | ✅        | Mật khẩu mới người dùng |

### Example Request
```json
{
  "email": "user@example.com",
  "old_password": "abc@123",
  "new_password": "xyz@456"
}
```