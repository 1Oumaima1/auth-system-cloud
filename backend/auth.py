from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import uuid
import smtplib
import ssl
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
import secrets
from datetime import datetime, timedelta
from urllib.parse import urlencode

# ===================== LOAD ENV =====================
load_dotenv()
import os

print("CURRENT DIR:", os.getcwd())
print("ENV EXISTS:", os.path.exists(".env"))
print("EMAIL_USER:", os.getenv("EMAIL_USER"))
print("EMAIL_PASS:", os.getenv("EMAIL_PASS"))

# ===================== CONFIG =====================
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

# ===================== SECURITY =====================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ===================== PASSWORD =====================
def hash_password(password: str):
    password = password[:72]  # 🔥 fix bcrypt limit
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password[:72], hashed_password)

# ===================== JWT =====================
def create_token(data: dict):
    data.update({
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    })
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

# ===================== PASSWORD RESET =====================
def generate_reset_token() -> tuple[str, datetime]:
    token = secrets.token_urlsafe(32)
    expiry = datetime.utcnow() + timedelta(minutes=15)
    return token, expiry

def send_reset_email(email: str, token: str, nom: str, expiry: datetime):
    if not EMAIL_USER or not EMAIL_PASS:
        raise HTTPException(status_code=500, detail="Email config missing")

    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = email
    msg["Subject"] = "Réinitialiser votre mot de passe"

    link = f"http://localhost:3000/reset-password?token={token}"

    body = f"""Bonjour {nom},

Cliquez pour réinitialiser votre mot de passe :

{link}

Le lien expire dans 15 minutes.
"""

    msg.attach(MIMEText(body, "plain"))

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

# ===================== AUTH =====================
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        return decode_token(token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_admin(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return payload

# ===================== EMAIL CONFIRMATION =====================
def generate_verification_token() -> str:
    return str(uuid.uuid4())

def send_verification_email(email: str, token: str, nom: str):
    # 1. Vérification des variables (Utilise les noms de ton .env)
    if not EMAIL_USER or not EMAIL_PASS:
        print("⚠️ Erreur : Configuration email manquante dans le .env")
        return # On sort pour ne pas faire planter tout le Signup

    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = email
    msg["Subject"] = "Vérifiez votre compte"

    # ⚠️ IMPORTANT : Remplace l'URL locale par ton URL Railway en production
    # Tu peux créer une variable d'environnement BASE_URL sur Railway
    base_url = os.getenv("BASE_URL", "https://auth-system-cloud-production.up.railway.app")
    link = f"{base_url}/auth/verify/{token}"

    body = f"""
Bonjour {nom},

Cliquez sur le lien pour vérifier votre compte :
{link}

Si ce n'est pas vous, ignorez cet email.
"""
    msg.attach(MIMEText(body, "plain"))

    try:
        # 2. Configuration sécurisée
        context = ssl.create_default_context()
        
        # Utilisation de 'with' pour s'assurer que la connexion se ferme
        with smtplib.SMTP(SMTP_HOST, int(SMTP_PORT), timeout=15) as server:
            server.starttls(context=context) # Sécurisation de la connexion
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
            print(f"✅ Email de vérification envoyé avec succès à {email}")
            
    except Exception as e:
        # On affiche l'erreur dans les logs Railway mais on ne bloque pas l'utilisateur
        print(f"❌ Erreur lors de l'envoi de l'email : {str(e)}")
