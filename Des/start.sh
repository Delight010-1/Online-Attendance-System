#!/bin/bash

echo "🚀 Starting University Attendance System..."
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Navigate to project directory
cd /workspace/Des

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt --break-system-packages
fi

# Run migrations
echo "🗄️  Running database migrations..."
python3 manage.py makemigrations
python3 manage.py migrate

# Populate sample data
echo "📊 Populating sample data..."
python3 manage.py populate_sample_data

# Get IP addresses
echo "🌐 Getting network information..."
HOST_IPS=$(hostname -I)
echo "Available IP addresses: $HOST_IPS"

echo ""
echo "🎯 STARTING SERVER..."
echo "====================="
echo "Server will be available at:"
echo ""
echo "📍 Local access:"
echo "   http://localhost:8000"
echo "   http://127.0.0.1:8000"
echo ""
echo "📍 Network access:"
for ip in $HOST_IPS; do
    echo "   http://$ip:8000"
done
echo ""
echo "🔑 Login Credentials:"
echo "====================="
echo "Super Admin:"
echo "   Username: superadmin@university.com"
echo "   Password: superadmin123"
echo ""
echo "Regular Admin:"
echo "   Username: admin@university.com"
echo "   Password: admin123"
echo ""
echo "Lecturer:"
echo "   Username: lecturer@university.com"
echo "   Password: lecturer123"
echo ""
echo "Student:"
echo "   Username: student@university.com"
echo "   Password: student123"
echo ""
echo "📱 Available URLs:"
echo "=================="
echo "• Home Page: http://localhost:8000/"
echo "• Login Portal: http://localhost:8000/login/"
echo "• Student Login: http://localhost:8000/student/login/"
echo "• Lecturer Login: http://localhost:8000/lecturer/login/"
echo "• Admin Login: http://localhost:8000/admin/login/"
echo "• Student Registration: http://localhost:8000/student/register/"
echo ""
echo "⚠️  IMPORTANT: If you can't access localhost, try the network IPs above"
echo "💡 If using Docker/Container: Use the network IP addresses shown above"
echo "🔧 To stop the server: Press Ctrl+C"
echo ""
echo "🚀 Starting Django development server..."
echo "======================================"

# Start the server
python3 manage.py runserver 0.0.0.0:8000