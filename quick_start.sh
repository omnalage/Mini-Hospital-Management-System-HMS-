#!/bin/bash

# Hospital Management System - Quick Start Script
# This script sets up the HMS project for development

set -e

echo "=========================================="
echo "HMS - Hospital Management System"
echo "Quick Start Setup"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
python3 --version
echo ""

# Backend Setup
echo -e "${YELLOW}Setting up Django Backend...${NC}"
cd hms_backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit .env with your PostgreSQL credentials${NC}"
fi

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser prompt
echo ""
echo -e "${YELLOW}Creating Django superuser...${NC}"
python manage.py createsuperuser

# Populate sample data
echo ""
read -p "Populate database with sample data? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Loading sample data..."
    python manage.py shell < populate_db.py
fi

echo ""
echo -e "${GREEN}=========================================="
echo "✓ Backend setup complete!"
echo "==========================================${NC}"
echo ""
echo "To start the server, run:"
echo "  cd hms_backend"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Access the application at:"
echo "  Home: http://localhost:8000/"
echo "  Admin: http://localhost:8000/admin"
echo ""
echo "For Serverless Email Service setup, see:"
echo "  serverless_email/README.md"
echo ""
