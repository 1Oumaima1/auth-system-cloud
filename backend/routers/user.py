from fastapi import APIRouter, Depends
from auth import get_current_user

router = APIRouter(prefix="/user")

@router.get("/data")
def get_user_data(current_user=Depends(get_current_user)):
    return {"msg": f"Welcome User {current_user.get('user_id')}"}