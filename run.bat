@echo off
echo Starting BookVerse...
set PYTHONDONTWRITEBYTECODE=1
uvicorn app.main:app --reload
