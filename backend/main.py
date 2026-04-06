# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import auth, admin, user

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
# Include routes
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(user.router)
