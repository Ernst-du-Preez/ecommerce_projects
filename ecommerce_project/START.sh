#!/bin/bash

echo "============================================"
echo "E-Commerce Platform Quick Start"
echo "============================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        echo "Make sure Python 3 is installed"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
if [ ! -d "venv/lib/python*/site-packages/django" ]; then
    echo "Installing dependencies... This may take a few minutes..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

# Check if database exists
if [ ! -f "db.sqlite3" ]; then
    echo "Setting up database..."
    python manage.py migrate
    echo ""
    echo "Creating admin user..."
    python manage.py createsuperuser
fi

# Start server
echo ""
echo "============================================"
echo "Starting development server..."
echo "============================================"
echo "Access the application at: http://127.0.0.1:8000/"
echo "Admin panel at: http://127.0.0.1:8000/admin/"
echo ""
echo "Press CTRL+C to stop the server"
echo "============================================"
echo ""

python manage.py runserver
