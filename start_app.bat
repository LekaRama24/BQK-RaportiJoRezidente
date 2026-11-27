@echo off
chcp 65001 >nul
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" goto run

echo Pergatitja e pare: krijohet mjedisi dhe instalohen paketat - zgjat 1-3 minuta...
py -3 -m venv .venv >nul 2>&1
if not exist ".venv\Scripts\python.exe" python -m venv .venv >nul 2>&1
if not exist ".venv\Scripts\python.exe" goto nopython
".venv\Scripts\python.exe" -m pip install --upgrade pip >nul
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto pipfail

:run
".venv\Scripts\python.exe" -m streamlit run app.py
pause
exit /b 0

:nopython
echo.
echo Python nuk u gjet ne kete kompjuter.
echo Instalojeni nga https://www.python.org/downloads/ - gjate instalimit zgjidhni "Add python.exe to PATH",
echo pastaj klikoni perseri dy here start_app.bat
pause
exit /b 1

:pipfail
echo.
echo Instalimi i paketave deshtoi - kontrolloni lidhjen me internet dhe provoni perseri.
rmdir /s /q .venv
pause
exit /b 1
