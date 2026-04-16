from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import Base, engine
from routers import auth, admin, user
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in .env")

Base.metadata.create_all(bind=engine)

app = FastAPI()

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

app.include_router(auth.router, prefix="/auth")
app.include_router(admin.router, prefix="/admin_api")
app.include_router(user.router, prefix="/user_api")


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
frontend_path = os.path.join(BASE_DIR, "frontend", "build")


print(f"--- DEBUG INFO ---")
print(f"Current Directory: {CURRENT_DIR}")
print(f"Project Root: {BASE_DIR}")
print(f"Target Frontend Path: {frontend_path}")
print(f"Frontend Path Exists: {os.path.exists(frontend_path)}")
print(f"--- --- --- --- ---")

if os.path.exists(frontend_path):
    
    app.mount("/static", StaticFiles(directory=os.path.join(frontend_path, "static")), name="static")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        
        if full_path.startswith(("auth", "admin_api", "user_api", "docs", "openapi.json")):
            return None 
        
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
        "frontend_status": "Build folder not found at " + frontend_path
    }
