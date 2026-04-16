from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserLogin, ForgotPassword, ResetPasswordWithToken
from datetime import datetime

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

# =============================
# ROUTER
# =============================
# On laisse vide car le préfixe "/auth" est défini dans main.py
router = APIRouter()

# =============================
# OAUTH GOOGLE
# =============================
oauth = OAuth()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# En production, Railway utilisera l'URL publique, en local il utilisera localhost
GOOGLE_REDIRECT_URI = os.getenv(
    "GOOGLE_REDIRECT_URI",
    "https://auth-system-cloud-production.up.railway.app/auth/google/callback"
)

oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"}
)

# =============================
# SIGNUP
# =============================
@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Cet email est déjà utilisé"
        )

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

    return {"msg": "Compte créé. Veuillez vérifier votre email."}

# =============================
# LOGIN
# =============================
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Identifiants invalides"
        )

    if not db_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Veuillez vérifier votre email avant de vous connecter"
        )

    token = create_token({
        "user_id": db_user.id,
        "role": db_user.role
    })

    return {
        "access_token": token,
        "role": db_user.role
    }

# =============================
# VERIFY EMAIL
# =============================
@router.get("/verify/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verification_token == token).first()

    if not user:
        raise HTTPException(status_code=400, detail="Token invalide")

    user.is_verified = True
    user.verification_token = None
    db.commit()

    return {"msg": "Email vérifié avec succès"}

# =============================
# FORGOT PASSWORD
# =============================
@router.post("/forgot-password")
def forgot_password(request: ForgotPassword, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        # Sécurité : on ne confirme pas si l'email existe ou non
        return {"msg": "Si l'email existe, un lien a été envoyé."}

    token, expiry = generate_reset_token()
    user.reset_token = token
    user.reset_expires_at = expiry
    db.commit()

    send_reset_email(user.email, token, user.nom, expiry)

    return {"msg": "Email de réinitialisation envoyé"}

# =============================
# RESET PASSWORD
# =============================
@router.post("/reset-password")
def reset_password(request: ResetPasswordWithToken, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.reset_token == request.token,
        User.reset_expires_at > datetime.utcnow()
    ).first()

    if not user:
        raise HTTPException(status_code=400, detail="Token invalide ou expiré")

    if request.password != request.confirm_password:
        raise HTTPException(status_code=400, detail="Les mots de passe ne correspondent pas")

    user.password = hash_password(request.password)
    user.reset_token = None
    user.reset_expires_at = None
    db.commit()

    return {"msg": "Mot de passe réinitialisé avec succès"}

# =============================
# GOOGLE LOGIN
# =============================
@router.get("/google")
async def google_login(request: Request):
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Configuration Google OAuth manquante")

    return await oauth.google.authorize_redirect(
        request,
        GOOGLE_REDIRECT_URI
    )

# =============================
# GOOGLE CALLBACK
# =============================
@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
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
    elif not user.google_id:
        user.google_id = google_id
        user.is_verified = True
    
    db.commit()
    db.refresh(user)

    jwt_token = create_token({
        "user_id": user.id,
        "role": user.role
    })

    # Redirection vers la racine du site (fonctionne en local et prod)
    return RedirectResponse(
        url=f"/?token={jwt_token}&role={user.role}"
    )
