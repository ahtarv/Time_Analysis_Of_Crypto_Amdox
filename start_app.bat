@echo off
echo ========================================
echo Cryptocurrency Analysis Platform
echo ========================================
echo.
echo Starting Backend API Server...
start "Flask API Backend" cmd /k "python api.py"
timeout /t 3 /nobreak > nul
echo.
echo Starting Frontend Development Server...
cd asset-forecaster-pro-main
start "React Frontend" cmd /k "npm run dev"
cd ..
echo.
echo ========================================
echo Both servers are starting...
echo Backend API: http://localhost:5000
echo Frontend: http://localhost:5173
echo ========================================
echo.
echo Press any key to exit...
pause > nul
