@echo off
echo ========================================
echo   Trading Intelligence Pro Startup
echo ========================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo Generating initial data...
python live_trading_backend.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to generate market data
    pause
    exit /b 1
)

echo.
echo Creating standalone dashboard...
python create_standalone_dashboard.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to create dashboard
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Choose your preferred option:
echo.
echo 1. Open Standalone Dashboard (No server required)
echo 2. Start Web Server (Full API + Multi-page site)
echo 3. Exit
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Opening standalone dashboard...
    start TradingIntelligence_Dashboard.html
    echo Dashboard opened in your default browser
    echo.
    echo To update data, run: python live_trading_backend.py
    echo Then run: python create_standalone_dashboard.py
) else if "%choice%"=="2" (
    echo.
    echo Starting web server...
    echo Server will be available at: http://localhost:5000
    echo Multi-page site available at: index.html
    echo.
    echo Press Ctrl+C to stop the server
    python app.py
) else if "%choice%"=="3" (
    echo Goodbye!
    exit /b 0
) else (
    echo Invalid choice. Please run the script again.
)

echo.
pause


