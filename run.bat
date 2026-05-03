@echo off
echo Starting BookVerse...
set PYTHONDONTWRITEBYTECODE=1
uvicorn app.app:app --reload
