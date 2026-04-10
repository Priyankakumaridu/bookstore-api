from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional
import os

# 🔐 Security settings
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")  # change in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ✅ Use bcrypt properly
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# ✅ Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ✅ Hash password (FIXED)
def get_password_hash(password: str) -> str:
    # 🔥 Handle bcrypt 72-byte limit safely
    password_bytes = password.encode("utf-8")
    
    if len(password_bytes) > 72:
        raise ValueError("Password too long (max 72 bytes allowed)")
    
    return pwd_context.hash(password)

# ✅ Create JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt