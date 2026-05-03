from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.database.db import users_collection
from app.utils.security import hash_password, verify_password, create_access_token

router = APIRouter()

# --- Pydantic Models ---
class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# --- Routes ---

@router.post("/signup")
def signup(user_data: UserSignup):
    """Signup a new user."""
    # 1. Check if user already exists (case-insensitive)
    if users_collection.find_one({"email": str(user_data.email).lower()}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 2. Hash password and store user
    new_user = {
        "name": str(user_data.name),
        "email": str(user_data.email).lower(),
        "password": hash_password(str(user_data.password)),
        "created_at": datetime.utcnow()
    }
    
    users_collection.insert_one(new_user)
    
    return {"message": "User registered successfully"}

@router.post("/login")
def login(user_data: UserLogin):
    """Login a user and return a JWT token."""
    # 1. Find user by email (normalize to lowercase)
    user = users_collection.find_one({"email": str(user_data.email).lower()})
    
    # 2. Verify existence and password
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Get stored password safely
    stored_password = str(user.get("password", ""))
    
    if not verify_password(str(user_data.password), stored_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # 3. Create JWT token
    token = create_access_token({"user_id": str(user["_id"]), "name": user["name"]})
    
    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }
