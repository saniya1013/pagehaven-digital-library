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
    Defensively handles length and encoding."""
    if not password:
        return ""
    # Ensure it's a string and truncate to 72 bytes safely
    safe_password = str(password)[:72]
    return pwd_context.hash(safe_password)

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against a hashed password.
    Extremely defensive to prevent '72 bytes' error on Render."""
    if not password or not hashed_password:
        return False
    
    try:
        # 1. Truncate plain password to 72 chars (bcrypt limit)
        safe_password = str(password)[:72]
        
        # 2. Check if hashed_password is a valid bcrypt hash
        # If it doesn't start with $2b$ or $2a$, it might be a legacy plain text
        if not str(hashed_password).startswith("$"):
            print("Warning: Detected unhashed password in DB. Comparing directly.")
            return safe_password == str(hashed_password)
            
        # 3. Verify using passlib
        return pwd_context.verify(safe_password, hashed_password)
    except Exception as e:
        print(f"Bcrypt Verify Error: {e} | Plain Length: {len(str(password))} | Hash starts with: {str(hashed_password)[:5]}")
        # Final fallback: direct comparison if it's somehow a plain text in the DB
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
