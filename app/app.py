from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

from app.routes.book_routes import router as book_router
from app.routes.auth import router as auth_router
from app.routes.user_routes import router as user_router

app = FastAPI(
    title="PageHaven API",
    description="Professional E-Library Backend",
    version="1.0.0"
)

# --- Middleware ---
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In strict production, replace with specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static (CSS + JS)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# --- Global Error Handlers ---
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return templates.TemplateResponse(request=request, name="index.html", status_code=404)

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    # Log the full error for Render logs
    print(f"ERROR 500: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": f"Server Error: {str(exc)}"}
    )

# Home page
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

# Dashboard page
@app.get("/home")
def dashboard_page(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")

# Book page
@app.get("/book")
def book_page(request: Request):
    return templates.TemplateResponse(request=request, name="book.html")

# Auth page (Login/Signup)
@app.get("/auth")
def auth_page(request: Request):
    return templates.TemplateResponse(request=request, name="auth.html")

@app.get("/profile")
def profile_page(request: Request):
    return templates.TemplateResponse(request=request, name="profile.html")

@app.get("/read")
def read_page(request: Request):
    return templates.TemplateResponse(request=request, name="reader.html")

# API routes
app.include_router(book_router)
app.include_router(auth_router)
app.include_router(user_router)