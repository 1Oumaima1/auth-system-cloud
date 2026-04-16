from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import Base, engine
from routers import auth, admin, user
from dotenv import load_dotenv
import os
import models
# --- 1. CONFIGURATION INITIALE ---
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in Railway Variables")

# Création des tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- 2. MIDDLEWARES ---
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://auth-system-cloud-production.up.railway.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    max_age=3600,
    same_site="lax"
)

# --- 3. ROUTES API (PRIORITÉ MAXIMALE) ---
# On les place AVANT le frontend pour éviter les erreurs 405
app.include_router(auth.router, prefix="/auth")
app.include_router(admin.router, prefix="/admin_api")
app.include_router(user.router, prefix="/user_api")

# --- 4. CONFIGURATION DU FRONTEND (MONOLITHIC) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_path = os.path.join(current_dir, "static")

if os.path.exists(frontend_path):
    # Montage des fichiers compilés (JS/CSS)
    react_static_path = os.path.join(frontend_path, "static")
    if os.path.exists(react_static_path):
        app.mount("/static", StaticFiles(directory=react_static_path), name="static")

    # Gestion des routes React et des fichiers physiques (manifest.json, etc.)
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # On ignore si c'est une route API ou de la doc
        if full_path.startswith(("auth", "admin_api", "user_api", "docs", "openapi.json", "static")):
            return None 
        
        # On vérifie si le fichier existe vraiment (ex: manifest.json, favicon.ico)
        potential_file = os.path.join(frontend_path, full_path)
        if os.path.isfile(potential_file):
            return FileResponse(potential_file)
        
        # Par défaut, on sert l'index.html pour le routing React
        index_file = os.path.join(frontend_path, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"error": "index.html not found"}

@app.get("/")
async def root():
    index_file = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "message": "Backend is running!",
        "frontend_status": "Static folder missing. Check your GitHub Action logs."
    }
