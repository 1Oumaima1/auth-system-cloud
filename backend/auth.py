from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import uuid
import smtplib
import ssl
import os
import secrets
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ===================== LOAD ENV =====================
load_dotenv()

# Configuration des variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587 # Port TLS standard

# ===================== SECURITY =====================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ===================== PASSWORD =====================
def hash_password(password: str):
    password = password[:72]  
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password[:72], hashed_password)

# ===================== JWT =====================
def create_token(data: dict):
    payload = data.copy()
    payload.update({
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    })
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

# ===================== EMAIL HELPER (POUR ÉVITER LES DOUBLONS) =====================
def _send_email_safe(recipient: str, subject: str, body: str):
    """Fonction utilitaire sécurisée pour envoyer des emails sur Railway"""
    if not EMAIL_USER or not EMAIL_PASS:
        print("⚠️ Config Email manquante")
        return False

    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        context = ssl.create_default_context()
        # On force le timeout et le port en entier
        with smtplib.SMTP(SMTP_HOST, int(SMTP_PORT), timeout=15) as server:
            server.starttls(context=context)
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
            return True
    except Exception as e:
        print(f"❌ Erreur SMTP : {e}")
        return False

# ===================== PASSWORD RESET =====================
def generate_reset_token() -> tuple[str, datetime]:
    token = secrets.token_urlsafe(32)
    expiry = datetime.utcnow() + timedelta(minutes=15)
    return token, expiry

def send_reset_email(email: str, token: str, nom: str, expiry: datetime):
    # Utilisation de l'URL Railway pour le frontend (à adapter selon ton port Flutter)
    base_url = os.getenv("FRONTEND_URL", "https://ton-app-flutter.up.railway.app")
    link = f"{base_url}/reset-password?token={token}"
    
    body = f"Bonjour {nom},\n\nCliquez pour réinitialiser votre mot de passe :\n{link}\n\nExpire dans 15 min."
    _send_email_safe(email, "Réinitialiser votre mot de passe", body)

# ===================== EMAIL CONFIRMATION =====================
def generate_verification_token() -> str:
    return str(uuid.uuid4())

def send_verification_email(email: str, token: str, nom: str):
    base_url = os.getenv("BASE_URL", "https://auth-system-cloud-production.up.railway.app")
    link = f"{base_url}/auth/verify/{token}"

    body = f"Bonjour {nom},\n\nCliquez ici pour vérifier votre compte :\n{link}"
    _send_email_safe(email, "Vérifiez votre compte", body)

# ===================== AUTH DEPENDENCIES =====================
def get_current_admin(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return payload
