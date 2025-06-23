@echo off
echo Starting Aura Vision Assistant...
echo.

echo Step 1: Installing frontend dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo Error installing frontend dependencies
    pause
    exit /b 1
)

echo Step 2: Building React app...
call npm run build
if %errorlevel% neq 0 (
    echo Error building React app
    pause
    exit /b 1
)

echo Step 3: Installing backend dependencies...
cd ..\backend
call npm install
if %errorlevel% neq 0 (
    echo Error installing backend dependencies
    pause
    exit /b 1
)

echo Step 4: Starting Python AI backend...
cd ..
start "Python Backend" cmd /k "uvicorn main_voice_simple:app --reload --port 8001"

echo Step 5: Starting Node.js frontend server...
cd backend
start "Node.js Frontend" cmd /k "npm start"

echo.
echo Aura Vision Assistant is starting...
echo.
echo Frontend: http://localhost:3000
echo Python API: http://localhost:8001
echo.
echo Press any key to exit this script...
pause > nul 