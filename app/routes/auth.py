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
    # 1. Check if user already exists
    if users_collection.find_one({"email": user_data.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 2. Hash password and store user
    new_user = {
        "name": user_data.name,
        "email": user_data.email,
        "password": hash_password(user_data.password),
        "created_at": datetime.utcnow()
    }
    
    users_collection.insert_one(new_user)
    
    return {"message": "User registered successfully"}

@router.post("/login")
def login(user_data: UserLogin):
    """Login a user and return a JWT token."""
    # 1. Find user by email
    user = users_collection.find_one({"email": user_data.email})
    
    # 2. Verify existence and password
    if not user or not verify_password(user_data.password, user["password"]):
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
