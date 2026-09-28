@echo off
title Fire and Smoke Detection System
echo ==========================================
echo   Fire and Smoke Detection System
echo ==========================================
if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv .venv
)
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Starting server...
python app.py
pause
