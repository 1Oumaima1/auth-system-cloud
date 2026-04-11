from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserLogin, ForgotPassword, ResetPassword, ResetPasswordWithToken

from auth import (
    hash_password,
    verify_password,
    create_token,
    generate_verification_token,
    send_verification_email,
    generate_reset_token,
    send_reset_email
)

from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from starlette.responses import RedirectResponse
import os

router = APIRouter(prefix="/auth")

# -----------------------------
# OAuth Setup
# -----------------------------
oauth = OAuth()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = "http://127.0.0.1:8000/auth/google/callback"



oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)

# -----------------------------
# SIGNUP
# -----------------------------
@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        return {"error": "Email already registered"}

    hashed = hash_password(user.password)
    token = generate_verification_token()

    new_user = User(
        nom=user.nom,
        prenom=user.prenom,
        email=user.email,
        password=hashed,
        role="user",
        is_verified=False,
        verification_token=token
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    send_verification_email(new_user.email, token, new_user.nom)

    return {"msg": "User created. Please verify email."}

# -----------------------------
# LOGIN
# -----------------------------
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        return {"error": "Invalid credentials"}

    if not db_user.is_verified:
        return {"error": "Please verify email first"}

    token = create_token({"user_id": db_user.id, "role": db_user.role})

    return {"access_token": token, "role": db_user.role}

# EMAIL VERIFY

@router.get("/verify/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verification_token == token).first()

    if not user:
        return {"error": "Invalid token"}

    user.is_verified = True
    user.verification_token = None
    db.commit()

    return {"msg": "Email verified"}

# -----------------------------
# FORGOT PASSWORD
# -----------------------------
@router.post("/forgot-password")
async def forgot_password(request: ForgotPassword, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        return {"msg": "If email exists, reset sent"}

    token, expiry = generate_reset_token()
    user.reset_token = token
    user.reset_expires_at = expiry
    db.commit()

    send_reset_email(user.email, token, user.nom, expiry)

    return {"msg": "Reset email sent"}

@router.post("/auth/reset-password")
async def reset_password(request: ResetPasswordWithToken, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.reset_token == request.token,
        User.reset_expires_at > datetime.utcnow()
    ).first()

    if not user:
        return {"error": "Invalid or expired token"}

    if request.password != request.confirm_password:
        return {"error": "Passwords do not match"}

    user.password = hash_password(request.password)
    user.reset_token = None
    user.reset_expires_at = None
    db.commit()

    return {"msg": "Password reset success"}

# -----------------------------
# GOOGLE LOGIN
# -----------------------------
@router.get("/google")
async def google_login(request: Request):
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Google OAuth not configured")

    return await oauth.google.authorize_redirect(
        request,
        GOOGLE_REDIRECT_URI
    )

# -----------------------------
# GOOGLE CALLBACK
# -----------------------------
@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Google OAuth not configured")

    token = await oauth.google.authorize_access_token(request)

    resp = await oauth.google.get(
        "https://openidconnect.googleapis.com/v1/userinfo",
        token=token
    )

    userinfo = resp.json()

    email = userinfo["email"]
    google_id = userinfo["sub"]
    name = userinfo.get("name", "User")

    parts = name.split(" ")
    nom = parts[0]
    prenom = " ".join(parts[1:]) if len(parts) > 1 else ""

    user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(
            nom=nom,
            prenom=prenom,
            email=email,
            google_id=google_id,
            role="user",
            is_verified=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    elif not user.google_id:
        user.google_id = google_id
        user.is_verified = True
        db.commit()

    jwt_token = create_token({"user_id": user.id, "role": user.role})

    return RedirectResponse(
        url=f"http://localhost:3000/?token={jwt_token}&role={user.role}"
    )