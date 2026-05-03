from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your_super_secret_key_change_this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hashes a plain-text password using bcrypt. 
    Truncates to 72 bytes to avoid bcrypt limitations."""
    # Bcrypt has a 72-byte limit. Truncating ensures it never fails.
    safe_password = password[:72]
    return pwd_context.hash(safe_password)

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against a hashed password.
    Truncates to 72 bytes to match hashing logic."""
    safe_password = password[:72]
    try:
        return pwd_context.verify(safe_password, hashed_password)
    except Exception:
        return False

def create_access_token(data: dict) -> str:
    """Creates a JWT access token with an expiration."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """Decodes a JWT token and returns the payload."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        return None
