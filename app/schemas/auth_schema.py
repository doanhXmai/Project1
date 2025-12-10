from pydantic import BaseModel, EmailStr

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class ResetPasswordRequest(BaseModel):
    access_token: str
    password: str

class LogoutRequest(BaseModel):
    refresh_token: str
# use email
class LoginRequestByEmail(BaseModel):
    email: EmailStr
    password: str

class RegisterRequestByEmail(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordRequestByEmail(BaseModel):
    email: str

class ChangePasswordRequestByEmail(BaseModel):
    email: EmailStr
    old_password: str
    new_password: str

# use phone
class LoginRequestByPhone(BaseModel):
    phone: EmailStr
    password: str

class RegisterRequestByPhone(BaseModel):
    phone: EmailStr
    password: str

class ForgotPasswordRequestByPhone(BaseModel):
    phone: str

class ChangePasswordRequestByPhone(BaseModel):
    phone: EmailStr
    old_password: str
    new_password: str