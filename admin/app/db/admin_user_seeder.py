#  seed or bootstrap data, to create an initial admin user
from app.db.database import SessionLocal
from app.models.models import AdminUser,UserRole
from app.core.utils import hash_password 

def create_admin_user():
    email = "admin@example.com"
    password = "secure_password"  # Fetch securely in real applications
    db = SessionLocal()

    try:
        # Check if admin already exists
        admin_user = db.query(AdminUser).filter(AdminUser.email == email).first()
        if admin_user:
            print(f"Admin user already exists: {admin_user.email}")
            return

        # Create admin user
        hashed_password = hash_password(password)
        new_admin = AdminUser(
            email=email,
            first_name="Admin",
            last_name="User",
            password=hashed_password,
            role=UserRole.ADMIN,
        )
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        print(f"Admin user created: {new_admin.email}")
    finally:
        db.close()

create_admin_user()