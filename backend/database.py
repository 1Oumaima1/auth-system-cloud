import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Récupération de l'URL depuis Railway
DATABASE_URL = os.getenv("DATABASE_URL")

# Fallback pour le développement local
if not DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:123@localhost/auth_db"

# Correction pour SQLAlchemy : on s'assure que l'URL commence par postgresql+psycopg
# Cela force l'utilisation du package psycopg (v3) que tu as installé
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

# Création de l'engine avec l'URL corrigée
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
