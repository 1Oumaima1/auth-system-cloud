from database import SessionLocal
from models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin():
    db = SessionLocal()
    hashed_password = pwd_context.hash("admin123")

    admin_user = User(
        nom="Admin",
        prenom="Super",
        email="admin@gmail.com",
        password=hashed_password,
        role="admin"
    )

    db.add(admin_user)
    db.commit()
    db.close()
    print("Admin created successfully")

if __name__ == "__main__":
    create_admin()