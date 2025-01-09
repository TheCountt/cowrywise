import bcrypt

def hash_password(password: str) -> str:
    """Hashes a plain-text password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against its hashed value."""
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
