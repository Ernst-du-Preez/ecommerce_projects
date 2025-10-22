@echo off
echo ============================================
echo E-Commerce Platform Quick Start
echo ============================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo Make sure Python is installed and added to PATH
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
if not exist "venv\Lib\site-packages\django\" (
    echo Installing dependencies... This may take a few minutes...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if database exists
if not exist "db.sqlite3" (
    echo Setting up database...
    python manage.py migrate
    echo.
    echo Creating admin user...
    python manage.py createsuperuser
)

REM Start server
echo.
echo ============================================
echo Starting development server...
echo ============================================
echo Access the application at: http://127.0.0.1:8000/
echo Admin panel at: http://127.0.0.1:8000/admin/
echo.
echo Press CTRL+C to stop the server
echo ============================================
echo.

python manage.py runserver

pause
