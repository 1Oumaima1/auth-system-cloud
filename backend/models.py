from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    prenom = Column(String)
    email = Column(String, unique=True, index=True)
    google_id = Column(String, nullable=True, unique=True)
    password = Column(String, nullable=True)
    role = Column(String, default="user")
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
    
    # AJOUTE CES DEUX LIGNES ICI :
    reset_token = Column(String, nullable=True)
    reset_expires_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
