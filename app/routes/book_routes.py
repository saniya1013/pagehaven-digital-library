from fastapi import APIRouter
from app.database.db import books_collection

router = APIRouter()


# ✅ GET ALL BOOKS
@router.get("/books")
def get_books():
    try:
        books = list(books_collection.find())

        result = []
        for book in books:
            result.append({
                "_id": str(book.get("_id")),
                "title": book.get("title", "No Title"),
                "author": book.get("author", "Unknown"),
                "category": book.get("category", []),
                "description": book.get("description", ""),
                "rating": book.get("rating", 0),
                "cover": book.get("cover", ""),
                "pdf_url": book.get("pdf_url", "")
            })

        return result

    except Exception as e:
        return {"error": str(e)}


# ✅ GET SINGLE BOOK (PRO VERSION - IMPORTANT)
from bson import ObjectId

@router.get("/book/{book_id}")
def get_book(book_id: str):
    try:
        book = books_collection.find_one({"_id": ObjectId(book_id)})

        if not book:
            return {"error": "Book not found"}

        return {
            "_id": str(book.get("_id")),
            "title": book.get("title", ""),
            "author": book.get("author", ""),
            "category": book.get("category", []),
            "description": book.get("description", ""),
            "rating": book.get("rating", 0),
            "cover": book.get("cover", ""),
            "pdf_url": book.get("pdf_url", "")
        }

    except Exception as e:
        return {"error": str(e)}