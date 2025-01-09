from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import admin_user_crud
from app.models.models import AdminUser
from app.db.database import get_db
from app.schemas.schemas import AdminUserCreate

router = APIRouter()

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_admin(admin_data: AdminUserCreate, db: Session = Depends(get_db)):
    """
    Create an admin user. Idempotent operation.
    """
    # Check if the admin user already exists
    existing_user = db.query(AdminUser).filter(AdminUser.email == admin_data.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Admin user with email {admin_data.email} already exists.",)
    
    # Create new admin
    new_admin = admin_user_crud.create_admin_user(admin_data, db)
    if new_admin is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating admin user. Please try again.",)
    return new_admin
