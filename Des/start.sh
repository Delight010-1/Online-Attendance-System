#!/bin/bash

echo "Starting University Attendance System..."
echo "======================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed or not in PATH"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "Error: manage.py not found. Please run this script from the Des directory."
    exit 1
fi

# Install dependencies if needed
echo "Checking dependencies..."
pip3 install -r requirements.txt --break-system-packages --quiet

# Run migrations
echo "Running database migrations..."
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

# Start the server
echo "Starting development server..."
echo "Access the application at: http://localhost:8000"
echo ""
echo "Login Credentials:"
echo "=================="
echo "Super Admin: superadmin / admin123"
echo "Regular Admin: admin@university.com / admin123"
echo "Lecturer: lecturer1 / lecturer123"
echo "Student: alice.johnson@student.university.com / student123"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 manage.py runserver 0.0.0.0:8000