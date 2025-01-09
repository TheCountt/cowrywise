from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.models import AdminUser, UserRole
from app.schemas.schemas import AdminUserCreate
from app.core.utils import hash_password


def create_admin_user(admin_data: AdminUserCreate, db: Session):
    """
    Create an admin user with exception handling.
    """
    try:
        # Hash the password (use a library like bcrypt for security)
        hashed_password = hash_password(admin_data.password)  # Replace with a secure hashing function
        
        # Create the admin user object
        admin_user = AdminUser(
            first_name=admin_data.first_name,
            last_name=admin_data.last_name,
            email=admin_data.email,
            password=hashed_password,
            role=UserRole.ADMIN,  # Assign admin role
        )
        
        # Add and commit to the database
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        return {
            "message": "Admin user created successfully",
            "email": admin_user.email,
        }

    except SQLAlchemyError as e:
        db.rollback()  # Rollback the transaction in case of an error
        print(f"Database error occurred: {e}") 
        
        # Raise an HTTPException with a meaningful message
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the admin user. Please try again later."
        )
    except Exception as e:
        db.rollback()  # Rollback for any other unexpected error
        print(f"Unexpected error occurred: {e}")  # Log the error
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please contact support."
        )
