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
### Example Response
```json
{
  "access_token": "your_access_token",
  "refresh_token": "your_refresh_token"
}
```

## 3. Refresh access token by email
**Method:** `POST`
**Endpoint:** `/api/v1/auth/refresh-access-token`
**Description:** Tạo mới access token sau mỗi lần request

### Request Body
| Filed          | Type    | Required | Description                        |
|----------------|---------|----------|------------------------------------|
| refresh_token  | string  | ✅        | token dùng để cấp lại access token |

### Example Request
```json
{
  "refresh_token": "your_refresh_token...."
}
```
### Example Response
```json
{
 "access_token": "your_access_token",
  "refresh_token": "your_refresh_token",
  "expires_in": "30"
}
```

## 4. Request Password Reset
**Method:** `POST`
**Endpoint:** `/api/v1/auth/request-password-reset`
**Description:** Lấy lại mật khẩu khi đã quên mật khẩu - nhận 1 mã OTP về email

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
### Example Response
#### status_code = 200
```json
{
  "status": true,
  "message": "OTP send successfully"
}
```
#### status_code = 404
```json
{
  "detail": "Email not found"
}
```

## 5. Verify OTP and Reset Password
**Method:** `POST`
**Endpoint:** `/api/v1/auth/verify-otp-reset-password`
**Description:** Thay đổi mật khẩu

### Request Body
| Filed        | Type    | Required | Description         |
|--------------|---------|----------|---------------------|
| email        | string  | ✅        | Email người dùng    |
| otp          | string  | ✅        | otp được gửi về     |
| new_password | string  | ✅        | mật khẩu mới để đổi |

### Example Request
```json
{
  "access_token": "youraccesstoken....",
  "password": "abc@123"
}
```
### Example Response
#### status_code = 200
```json
{
  "message": "OTP verified successfully",
  "email": "your_email@gmail.com",
  "success": true
}
```
#### status_code = 400
```json
{
  "detail": "Invalid OTP"
}
```
```json
{
  "detail": "OTP expired"
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
### Example Response
#### status_code = 200
```json
{
  "message": "Password changed successfully"
}
```
#### status_code = 401
```json
{
  "detail": "Old password is incorrect"
}
```