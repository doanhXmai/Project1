from pydantic import BaseModel

class LoginRequest(BaseModel):
    login_type: str
    value: str
    password: str