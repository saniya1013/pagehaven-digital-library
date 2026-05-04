from fastapi import APIRouter, HTTPException, Depends
from app.database.db import reading_history_collection, books_collection
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from bson import ObjectId

router = APIRouter(prefix="/reading-history", tags=["History"])

class HistorySaveRequest(BaseModel):
    user_id: str
    book_id: str
    last_page: Optional[int] = 0

@router.post("/save")
async def save_history(request: HistorySaveRequest):
    try:
        # Fetch book title for the history entry
        book = books_collection.find_one({"_id": ObjectId(request.book_id)})
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        history_data = {
            "user_id": request.user_id,
            "book_id": request.book_id,
            "book_title": book.get("title", "Unknown Title"),
            "book_author": book.get("author", "Unknown Author"),
            "cover": book.get("cover", ""),
            "last_page": request.last_page,
            "last_accessed": datetime.utcnow()
        }

        # Upsert: Update if user_id + book_id exists, else create
        reading_history_collection.update_one(
            {"user_id": request.user_id, "book_id": request.book_id},
            {"$set": history_data},
            upsert=True
        )
        return {"status": "success", "message": "History saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}")
async def get_history(user_id: str):
    try:
        # Get latest 4 books for the "Continue Reading" section
        history = list(reading_history_collection.find(
            {"user_id": user_id}
        ).sort("last_accessed", -1).limit(4))

        for item in history:
            item["_id"] = str(item["_id"])
        
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
