# schemas.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class ForgotPassword(BaseModel):
    email: str

class ResetPassword(BaseModel):
    password: str
    confirm_password: str

class ResetPasswordWithToken(BaseModel):
    token: str
    password: str
    confirm_password: str

class OAuthUser(BaseModel):
    email: str
    nom: str | None = None
    prenom: str | None = None
