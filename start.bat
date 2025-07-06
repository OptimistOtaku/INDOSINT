@echo off
echo Starting INDOSINT - AI-Powered OSINT System for India
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed or not in PATH
    echo Please install Node.js 16+ and try again
    pause
    exit /b 1
)

echo.
echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install Python dependencies
    pause
    exit /b 1
)

echo.
echo Installing Node.js dependencies...
cd frontend
npm install
if errorlevel 1 (
    echo Error: Failed to install Node.js dependencies
    pause
    exit /b 1
)
cd ..

echo.
echo Initializing database...
python run.py init-db
if errorlevel 1 (
    echo Error: Failed to initialize database
    pause
    exit /b 1
)

echo.
echo Starting the application...
echo Backend will be available at: http://localhost:5000
echo Frontend will be available at: http://localhost:3000
echo.
echo Press Ctrl+C to stop both servers
echo.

REM Start backend in a new window
start "INDOSINT Backend" cmd /k "python run.py run"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in a new window
start "INDOSINT Frontend" cmd /k "cd frontend && npm start"

echo.
echo Both servers are starting...
echo Please wait a moment for them to fully load.
echo.
echo Demo Accounts:
echo Admin: admin@indosint.com / admin123
echo Analyst: analyst@indosint.com / analyst123
echo User: user@indosint.com / user123
echo.
pause 