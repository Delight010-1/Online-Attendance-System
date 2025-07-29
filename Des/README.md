# University Attendance System

A comprehensive web-based attendance management system built with Django, featuring QR code scanning, role-based access control, and real-time attendance tracking.

## Features

### User Roles
- **Students**: Register, view attendance history, display QR codes
- **Lecturers**: Mark attendance via QR scanning or manual entry
- **Admins**: Manage courses, departments, levels, and generate reports
- **Super Admins**: Full system access including admin management

### Key Features
- QR Code generation and live scanning
- Real-time attendance tracking
- Role-based access control
- Beautiful, responsive UI with animations
- Comprehensive reporting system
- Timetable management
- Student registration and management

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Des
   ```

2. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt --break-system-packages
   ```

3. **Run migrations**
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

4. **Start the development server**
   ```bash
   python3 manage.py runserver 0.0.0.0:8000
   ```

5. **Access the application**
   Open your browser and navigate to: `http://localhost:8000`

## Login Credentials

### Super Admin
- **Username**: superadmin
- **Password**: admin123
- **Access**: Full system control, can manage other admins

### Regular Admin
- **Username**: admin@university.com
- **Password**: admin123
- **Access**: Course, department, and level management

### Lecturer
- **Username**: lecturer1
- **Password**: lecturer123
- **Access**: Mark attendance, view assigned courses

### Student
- **Username**: alice.johnson@student.university.com
- **Password**: student123
- **Access**: View attendance history, display QR code

## System Overview

### Student Features
- Registration with matric number, department, and level
- Automatic QR code generation
- View attendance history and timetable
- Display QR code for scanning

### Lecturer Features
- Live QR code scanning via web camera
- Manual attendance marking with checkboxes
- View assigned courses and levels
- Edit attendance records

### Admin Features
- Manage departments, levels, courses, and lecturers
- Generate attendance reports
- Create printable timetables
- View system statistics

### Super Admin Features
- All admin capabilities
- Create and manage other admins
- Full system oversight
- Generate system-wide reports

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **QR Code**: qrcode library
- **QR Scanning**: jsQR library
- **UI Framework**: Bootstrap 5 with custom animations

## Project Structure

```
Des/
├── attendance_system/     # Django project settings
├── core/                 # Main application
│   ├── models.py        # Database models
│   ├── views.py         # View logic
│   ├── forms.py         # Form definitions
│   ├── urls.py          # URL routing
│   └── templates/       # HTML templates
├── static/              # Static files (CSS, JS)
├── templates/           # Base templates
└── manage.py           # Django management script
```

## Key URLs

- **Home**: `/`
- **Student Login**: `/student/login/`
- **Lecturer Login**: `/lecturer/login/`
- **Admin Login**: `/admin/login/`
- **Student Dashboard**: `/student/dashboard/`
- **Lecturer Dashboard**: `/lecturer/dashboard/`
- **Admin Dashboard**: `/admin/dashboard/`
- **Super Admin Dashboard**: `/super-admin/dashboard/`

## QR Code System

Each student is assigned a unique QR code during registration. The QR code contains:
- Student ID
- Matric number
- Format: `STUDENT:STUDENT_ID:MATRIC_NUMBER`

Lecturers can scan these QR codes using the web application's built-in camera scanner to automatically mark attendance.

## Reporting System

The system includes comprehensive reporting features:
- Filter by department, level, course, date range
- Export to Excel
- Print-friendly reports
- Real-time statistics

## Security Features

- Role-based access control
- Password encryption
- Session management
- CSRF protection
- Input validation

## Browser Compatibility

- Chrome (recommended for QR scanning)
- Firefox
- Safari
- Edge

## Development

To add sample data for testing:
```bash
python3 manage.py populate_sample_data
```

## License

This project is developed for educational purposes.

## Support

For technical support or questions, please refer to the project documentation or contact the development team.