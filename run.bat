@echo off
cd backend

:: Check if virtual environment exists, create if not
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate venv and install requirements
call venv\Scripts\activate.bat
pip install -r requirements.txt

:: Run the program
python cli.py

:: Keep terminal open
pause