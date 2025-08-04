# University Attendance System

A modern, comprehensive web-based attendance management system built with Django that replaces traditional paper-based attendance tracking with a fast, reliable, and user-friendly digital solution.

## 🌟 Features

### For Students
- **Easy Registration** - Register with name, matric number, department, level, email, and password
- **Unique QR Code** - Automatically generated personal QR code for quick attendance marking
- **Dashboard** - View attendance history and class timetables
- **Mobile Friendly** - Responsive design works on all devices

### For Lecturers
- **Live QR Scanning** - Mark attendance using the built-in QR code scanner
- **Manual Entry** - Traditional checkbox-based attendance marking as backup
- **Real-time Updates** - Instant attendance tracking with timestamps
- **Course Management** - View assigned courses and student lists

### For Admins
- **Comprehensive Management** - Manage courses, lecturers, departments, levels, and timetables
- **Attendance Reports** - Generate detailed reports with filtering options
- **Data Export** - Export attendance data to Excel/PDF formats
- **Print-Ready Reports** - Professional printable timetables and attendance records

### For Super Admins
- **Full System Control** - All admin capabilities plus user management
- **Admin Creation** - Create and manage other administrators
- **System Overview** - Complete dashboard with system health and statistics

## 🚀 Technology Stack

- **Backend**: Django 4.2.7 with Python 3.13
- **Frontend**: HTML5, CSS3, JavaScript with Bootstrap 5
- **Database**: SQLite (easily configurable for PostgreSQL/MySQL)
- **QR Code**: qrcode library with live camera scanning
- **UI Framework**: Bootstrap 5 with custom animations
- **Icons**: Font Awesome 6

## 📋 System Requirements

- Python 3.8+
- Django 4.2+
- Modern web browser with camera support (for QR scanning)
- Internet connection (for CDN resources)

## 🛠️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd attendance-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Populate with sample data** (optional)
   ```bash
   python manage.py populate_data --clear
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the system**
   - Open your browser and navigate to `http://localhost:8000`

## 👥 Demo Accounts

The system comes with pre-populated demo accounts for testing:

### Super Admin
- **Username**: SUPER001
- **Password**: admin123
- **Access**: Full system administration

### Regular Admin
- **Username**: ADMIN001
- **Password**: admin123
- **Access**: System management (excluding admin creation)

### Sample Lecturer
- **Name**: Dr. Alice Johnson
- **Password**: lecturer123
- **Access**: Course and attendance management

### Sample Student
- **Email**: john.smith0@student.university.edu
- **Password**: student123
- **Access**: View attendance and QR code

## 🎯 Key Features Walkthrough

### 1. Student Registration & QR Code
- Students register with their academic details
- System automatically generates unique student ID and QR code
- QR codes contain encrypted student identification data

### 2. Live QR Code Scanning
- Lecturers use built-in camera to scan student QR codes
- Real-time attendance marking with instant feedback
- Fallback to manual entry when needed

### 3. Comprehensive Dashboards
- **Student Dashboard**: Attendance history, timetable, QR code access
- **Lecturer Dashboard**: Course overview, attendance marking tools
- **Admin Dashboard**: System statistics, management tools
- **Super Admin Dashboard**: Complete system oversight

### 4. Advanced Reporting
- Filter by department, level, course, date range
- Export to Excel and PDF formats
- Print-ready professional reports
- Real-time statistics and analytics

### 5. Beautiful UI/UX
- Modern gradient designs and animations
- Responsive layout for all screen sizes
- Intuitive navigation and user flows
- Loading animations and smooth transitions

## 🔧 Configuration

### Database Configuration
The system uses SQLite by default. To use PostgreSQL or MySQL:

1. Install the appropriate database adapter
2. Update `DATABASES` in `settings.py`
3. Run migrations: `python manage.py migrate`

### Media Files
QR codes are stored in `media/qr_codes/`. Ensure the media directory is writable.

### Email Configuration (Optional)
Update email settings in `settings.py` for password reset functionality.

## 📱 Mobile Usage

The system is fully responsive and optimized for mobile devices:
- Students can access their QR codes on mobile
- Lecturers can scan QR codes using mobile cameras
- All dashboards adapt to mobile screen sizes

## 🔒 Security Features

- **Password Encryption**: All passwords are hashed using Django's built-in security
- **Role-based Access Control**: Strict permissions for different user types
- **Session Management**: Secure session handling with automatic timeout
- **CSRF Protection**: Protection against cross-site request forgery
- **QR Code Security**: Encrypted student data in QR codes

## 🎨 UI/UX Features

- **Modern Design**: Clean, professional interface with gradient backgrounds
- **Smooth Animations**: Page transitions and loading animations
- **Interactive Elements**: Hover effects and button animations
- **Color-coded Status**: Visual indicators for attendance status
- **Loading States**: Beautiful loading screens with university branding

## 📊 System Architecture

```
├── attendance_system/     # Django project settings
├── core/                 # Main application
│   ├── models.py        # Database models
│   ├── views.py         # View controllers
│   ├── forms.py         # Form definitions
│   ├── urls.py          # URL routing
│   └── management/      # Custom management commands
├── templates/           # HTML templates
├── static/             # CSS, JavaScript, images
├── media/              # User uploaded files (QR codes)
└── requirements.txt    # Python dependencies
```

## 🐛 Troubleshooting

### Common Issues

1. **QR Scanner not working**
   - Ensure HTTPS is enabled for camera access
   - Check browser permissions for camera usage
   - Verify the QR code library is loaded correctly

2. **Media files not displaying**
   - Check `MEDIA_URL` and `MEDIA_ROOT` settings
   - Ensure media directory has proper permissions
   - Verify static files are served correctly

3. **Database errors**
   - Run `python manage.py migrate` to apply pending migrations
   - Check database file permissions (for SQLite)

## 🔄 Future Enhancements

- **Mobile App**: Native Android/iOS applications
- **Biometric Integration**: Fingerprint scanning for attendance
- **Advanced Analytics**: Machine learning for attendance patterns
- **Integration APIs**: Connect with existing university systems
- **Offline Support**: Sync attendance when internet is restored
- **Multi-language Support**: Internationalization capabilities

## 📞 Support

For technical support or feature requests:
- Create an issue in the repository
- Contact the development team
- Check the documentation for common solutions

## 📄 License

This project is developed for educational and institutional use. Please refer to the license file for usage terms.

---

**Built with ❤️ for modern educational institutions**

*Transforming attendance tracking from paper to digital excellence*