# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from database import Base, engine
from routers import auth, admin, user
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in .env")

# Create tables
Base.metadata.create_all(bind=engine)
app = FastAPI()
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# 3. Add the middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Add SessionMiddleware BEFORE routers
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    max_age=3600,
    same_site="lax"
)

# Include routes
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(user.router)
