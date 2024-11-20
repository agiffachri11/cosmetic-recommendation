from pydantic import BaseModel, EmailStr
from typing import Optional

class UserResponse(BaseModel):
    uid: str
    email: str
    name: Optional[str] = None
    photo_url: Optional[str] = None

class ErrorResponse(BaseModel):
    detail: str

class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr