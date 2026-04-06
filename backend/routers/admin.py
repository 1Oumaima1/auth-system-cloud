# routes/admin.py
from fastapi import APIRouter, Depends
from auth import get_current_admin

router = APIRouter(prefix="/admin")

@router.get("/data")
def admin_data(admin=Depends(get_current_admin)):
    return {"msg": f"Welcome Admin {admin['user_id']}"}