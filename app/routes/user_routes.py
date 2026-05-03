from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, status
from typing import Optional
import os
import shutil
from datetime import datetime
from bson import ObjectId
from app.database.db import users_collection
from app.utils.security import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()

UPLOAD_DIR = "app/static/uploads/profile_pics"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def get_current_user(auth: HTTPAuthorizationCredentials = Depends(security)):
    """Dependency to get the current user from JWT token."""
    payload = decode_access_token(auth.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in token"
        )
    
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.get("/user/me")
async def get_me(user: dict = Depends(get_current_user)):
    """Return current user details."""
    user["_id"] = str(user["_id"])
    del user["password"]
    return user

@router.put("/user/update")
async def update_user(
    name: str = Form(...),
    bio: Optional[str] = Form(None),
    favorite_category: Optional[str] = Form(None),
    user: dict = Depends(get_current_user)
):
    """Update user information."""
    update_data = {
        "name": name,
        "bio": bio or "",
        "favorite_category": favorite_category or ""
    }
    
    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": update_data}
    )
    
    return {"message": "Profile updated successfully"}

@router.post("/user/upload-profile-pic")
async def upload_profile_pic(
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user)
):
    """Upload and set profile picture."""
    # 1. Validate file type
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPG and PNG images are allowed"
        )
    
    # 2. Save file locally
    file_ext = os.path.splitext(file.filename)[1]
    filename = f"user_{user['_id']}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 3. Update DB with URL
    pic_url = f"/static/uploads/profile_pics/{filename}"
    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"profile_pic": pic_url}}
    )
    
    return {"message": "Profile picture updated", "profile_pic": pic_url}
