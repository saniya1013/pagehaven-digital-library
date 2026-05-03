import bcrypt
from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your_super_secret_key_change_this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days

def hash_password(password: str) -> str:
    """Hashes a plain-text password using native bcrypt library."""
    if not password:
        return ""
    # Ensure it's bytes and truncate to 72 to be safe
    pwd_bytes = str(password)[:72].encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against a hashed password using native bcrypt."""
    if not password or not hashed_password:
        return False
    
    try:
        # Convert to bytes
        pwd_bytes = str(password)[:72].encode('utf-8')
        hashed_bytes = str(hashed_password).encode('utf-8')
        
        # Check if it looks like a bcrypt hash (starts with $2b$ or $2a$)
        if not str(hashed_password).startswith("$"):
            return str(password) == str(hashed_password)
            
        return bcrypt.checkpw(pwd_bytes, hashed_bytes)
    except Exception as e:
        print(f"Direct Bcrypt Error: {e}")
        # Final fallback
        return str(password) == str(hashed_password)

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
