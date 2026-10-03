@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Set up the environment first by running these commands in this folder:
    echo py -m venv .venv
    echo .venv\Scripts\python.exe -m pip install -r requirements.txt
    echo .venv\Scripts\python.exe manage.py migrate
    pause
    exit /b 1
)

start "Django server" /D "%~dp0" ".venv\Scripts\python.exe" manage.py runserver 127.0.0.1:8010
timeout /t 2 /nobreak >nul
start "" http://127.0.0.1:8010/
