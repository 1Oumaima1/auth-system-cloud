# routes/auth.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserLogin
from auth import hash_password, verify_password, create_token
from database import Base, engine, get_db

router = APIRouter(prefix="/auth")

# Signup user (only user)
@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        return {"error": "Email already registered"}

    hashed = hash_password(user.password)
    new_user = User(
        nom=user.nom,
        prenom=user.prenom,
        email=user.email,
        password=hashed,
        role="user"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User created", "user_id": new_user.id}

# Login user/admin
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        return {"error": "Invalid credentials"}

    token = create_token({"user_id": db_user.id, "role": db_user.role})
    return {"access_token": token, "role": db_user.role}