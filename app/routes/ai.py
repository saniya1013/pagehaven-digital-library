from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import requests
from io import BytesIO
from pypdf import PdfReader
from groq import Groq
from app.database.db import books_collection
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/ai", tags=["AI Integration"])

# Configure Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)
else:
    client = None

class ChatRequest(BaseModel):
    book_id: str
    message: str

class SummarizeRequest(BaseModel):
    book_id: str

def extract_text_from_url(url: str, max_chars: int = 10000):
    """Downloads content from URL and extracts text. Supports PDFs and Gutenberg HTML."""
    try:
        # Handle Project Gutenberg links by getting the plain text version if possible
        if "gutenberg.org/ebooks/" in url:
            # Get the ID reliably even if there's a trailing slash
            book_id = url.rstrip('/').split('/')[-1]
            url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
            print(f"Transformed Gutenberg URL to: {url}")
        
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        # If it's plain text (Gutenberg cache)
        if url.endswith(".txt") or "text/plain" in response.headers.get("Content-Type", ""):
            return response.text[:max_chars]
            
        # If it's a PDF
        pdf_file = BytesIO(response.content)
        reader = PdfReader(pdf_file)
        
        text = ""
        for page in reader.pages:
            text += (page.extract_text() or "") + " "
            if len(text) > max_chars:
                break
        
        return text[:max_chars].strip()
    except Exception as e:
        print(f"Extraction Error for {url}: {e}")
        return None

@router.post("/summarize")
async def summarize_book(req: SummarizeRequest):
    print(f"AI SUMMARIZE REQUEST: {req.book_id}")
    if not client:
        raise HTTPException(status_code=500, detail="AI Service not configured (Missing GROQ_API_KEY)")
    
    try:
        book = books_collection.find_one({"_id": ObjectId(req.book_id)})
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        # Try to get book content, fallback to description
        print(f"Fetching context for: {book.get('title')}")
        content = extract_text_from_url(book.get("pdf_url", ""))
        context = content if content and len(content) > 100 else book.get("description", "No description available.")
        
        print("Sending to Groq...")
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an expert literary assistant. Summarize the provided book clearly with key takeaways. Use a professional and engaging tone."},
                {"role": "user", "content": f"Book Title: {book.get('title')}\nAuthor: {book.get('author')}\n\nContent/Description: {context}"}
            ],
            temperature=0.5,
            max_tokens=1024
        )
        print("Groq response received.")
        return {"summary": completion.choices[0].message.content}
    except Exception as e:
        print(f"AI ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal AI Error: {str(e)}")

@router.post("/chat")
async def chat_with_book(req: ChatRequest):
    print(f"AI CHAT REQUEST: {req.book_id} - '{req.message}'")
    if not client:
        raise HTTPException(status_code=500, detail="AI Service not configured (Missing GROQ_API_KEY)")
    
    try:
        book = books_collection.find_one({"_id": ObjectId(req.book_id)})
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        # Try to get book content, fallback to description
        print(f"Fetching context for: {book.get('title')}")
        content = extract_text_from_url(book.get("pdf_url", ""))
        context = content if content and len(content) > 100 else book.get("description", "No description available.")
        
        print("Sending to Groq...")
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": f"You are an AI assistant for the book '{book.get('title')}' by {book.get('author')}. Use the provided context to answer questions accurately. If you don't know the answer from the context, use your general knowledge about this famous book."},
                {"role": "user", "content": f"Context: {context}\n\nUser Question: {req.message}"}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        print("Groq response received.")
        return {"response": completion.choices[0].message.content}
    except Exception as e:
        print(f"AI ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal AI Error: {str(e)}")
