from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.routes.book_routes import router as book_router

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
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates (HTML)
templates = Jinja2Templates(directory="app/templates")

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

# API routes
app.include_router(book_router)