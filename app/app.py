from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

print("App starting...")
print("BASE DIR:", os.path.dirname(os.path.abspath(__file__)))
print("Templates exists:", os.path.exists(os.path.join(os.path.dirname(__file__), "templates")))
print("Static exists:", os.path.exists(os.path.join(os.path.dirname(__file__), "static")))
print("Mongo URL:", os.getenv("MONGO_URL"))

from app.routes.book_routes import router as book_router
from app.routes.auth import router as auth_router
from app.routes.user_routes import router as user_router

app = FastAPI()

# CORS (safe for now)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static (CSS + JS)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Home page
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Dashboard page
@app.get("/home")
def dashboard_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Book page
@app.get("/book")
def book_page(request: Request):
    return templates.TemplateResponse("book.html", {"request": request})

# Auth page (Login/Signup)
@app.get("/auth")
def auth_page(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})

@app.get("/profile")
def profile_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

@app.get("/read")
def read_page(request: Request):
    return templates.TemplateResponse("reader.html", {"request": request})

# API routes
app.include_router(book_router)
app.include_router(auth_router)
app.include_router(user_router)