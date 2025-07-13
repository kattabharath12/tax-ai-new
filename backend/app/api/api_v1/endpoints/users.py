from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...models.user import User

router = APIRouter()

@router.get("/profile")
async def get_user_profile(user_id: int = 1, db: Session = Depends(get_db)):
    """Get user profile"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": user.phone,
        "is_verified": user.is_verified
    }

@router.put("/profile")
async def update_user_profile(
    first_name: str = None,
    last_name: str = None,
    phone: str = None,
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    """Update user profile"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if phone:
        user.phone = phone

    db.commit()
    db.refresh(user)

    return {"message": "Profile updated successfully"}
