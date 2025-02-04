from pydantic import BaseModel, EmailStr
from typing import Dict


class GoogleLoginRequest(BaseModel):
    googleId: str
    email: EmailStr
    name: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    applications: Dict[str, str]  # Ejemplo: {"app1": "admin", "app2": "viewer"}

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    applications: Dict[str, str]

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    