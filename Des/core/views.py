from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import datetime, date
import json

from .models import *
from .forms import *

def is_student(user):
    return user.is_authenticated and user.user_type == 'student'

def is_lecturer(user):
    return user.is_authenticated and user.user_type == 'lecturer'

def is_admin(user):
    return user.is_authenticated and user.user_type == 'admin'

def is_super_admin(user):
    return user.is_authenticated and user.user_type == 'super_admin'

def home(request):
    return render(request, 'core/home.html')

def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to the attendance system.')
            return redirect('student_dashboard')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'core/student_register.html', {'form': form})

def student_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        
        if user and user.user_type == 'student':
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not a student account.')
    
    return render(request, 'core/student_login.html')

def lecturer_login(request):
    if request.method == 'POST':
        form = LecturerLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome, {user.get_full_name()}!')
            return redirect('lecturer_dashboard')
    else:
        form = LecturerLoginForm()
    
    return render(request, 'core/lecturer_login.html', {'form': form})

def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome, {user.get_full_name()}!')
            if user.user_type == 'super_admin':
                return redirect('super_admin_dashboard')
            else:
                return redirect('admin_dashboard')
    else:
        form = AdminLoginForm()
    
    return render(request, 'core/admin_login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    student = request.user.student_profile
    attendance_records = Attendance.objects.filter(student=student).order_by('-date')[:10]
    
    today = timezone.now().strftime('%A').lower()
    today_timetable = Timetable.objects.filter(
        department=student.department,
        level=student.level,
        day=today
    ).order_by('start_time')
    
    context = {
        'student': student,
        'attendance_records': attendance_records,
        'today_timetable': today_timetable,
    }
    return render(request, 'core/student_dashboard.html', context)

@login_required
@user_passes_test(is_lecturer)
def lecturer_dashboard(request):
    lecturer = request.user.lecturer_profile
    courses = Course.objects.filter(lecturer=lecturer)
    
    today = timezone.now().strftime('%A').lower()
    today_courses = Timetable.objects.filter(
        course__lecturer=lecturer,
        day=today
    ).order_by('start_time')
    
    context = {
        'lecturer': lecturer,
        'courses': courses,
        'today_courses': today_courses,
    }
    return render(request, 'core/lecturer_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    admin = request.user.admin_profile
    total_students = Student.objects.count()
    total_lecturers = Lecturer.objects.count()
    total_courses = Course.objects.count()
    total_attendance = Attendance.objects.count()
    
    context = {
        'admin': admin,
        'total_students': total_students,
        'total_lecturers': total_lecturers,
        'total_courses': total_courses,
        'total_attendance': total_attendance,
    }
    return render(request, 'core/admin_dashboard.html', context)

@login_required
@user_passes_test(is_super_admin)
def super_admin_dashboard(request):
    admin = request.user.admin_profile
    total_students = Student.objects.count()
    total_lecturers = Lecturer.objects.count()
    total_courses = Course.objects.count()
    total_attendance = Attendance.objects.count()
    total_admins = Admin.objects.count()
    total_departments = Department.objects.count()
    total_levels = Level.objects.count()
    today_attendance = Attendance.objects.filter(date=date.today()).count()
    
    context = {
        'admin': admin,
        'total_students': total_students,
        'total_lecturers': total_lecturers,
        'total_courses': total_courses,
        'total_attendance': total_attendance,
        'total_admins': total_admins,
        'total_departments': total_departments,
        'total_levels': total_levels,
        'today_attendance': today_attendance,
    }
    return render(request, 'core/super_admin_dashboard.html', context)

@login_required
@user_passes_test(is_student)
def student_qr_code(request):
    student = request.user.student_profile
    return render(request, 'core/student_qr_code.html', {'student': student})

@login_required
@user_passes_test(is_student)
def attendance_history(request):
    student = request.user.student_profile
    attendance_records = Attendance.objects.filter(student=student).order_by('-date')
    
    context = {
        'student': student,
        'attendance_records': attendance_records,
    }
    return render(request, 'core/attendance_history.html', context)

@login_required
@user_passes_test(is_student)
def timetable_view(request):
    student = request.user.student_profile
    timetable = Timetable.objects.filter(
        department=student.department,
        level=student.level
    ).order_by('day', 'start_time')
    
    context = {
        'student': student,
        'timetable': timetable,
    }
    return render(request, 'core/timetable_view.html', context)

@login_required
@user_passes_test(is_lecturer)
def mark_attendance(request, course_id):
    course = get_object_or_404(Course, id=course_id, lecturer=request.user.lecturer_profile)
    students = Student.objects.filter(department=course.department, level=course.level)
    
    if request.method == 'POST':
        date_str = request.POST.get('date')
        attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else date.today()
        
        for student in students:
            status = request.POST.get(f'status_{student.id}', 'absent')
            notes = request.POST.get(f'notes_{student.id}', '')
            
            attendance, created = Attendance.objects.get_or_create(
                student=student,
                course=course,
                date=attendance_date,
                defaults={
                    'status': status,
                    'marked_by': request.user.lecturer_profile,
                    'notes': notes
                }
            )
            
            if not created:
                attendance.status = status
                attendance.notes = notes
                attendance.save()
        
        messages.success(request, f'Attendance marked successfully for {course.code}')
        return redirect('lecturer_dashboard')
    
    context = {
        'course': course,
        'students': students,
        'today': date.today(),
    }
    return render(request, 'core/mark_attendance.html', context)

@login_required
@user_passes_test(is_lecturer)
def qr_scanner(request, course_id):
    course = get_object_or_404(Course, id=course_id, lecturer=request.user.lecturer_profile)
    return render(request, 'core/qr_scanner.html', {'course': course})

@csrf_exempt
def process_qr_scan(request, course_id):
    try:
        data = json.loads(request.body)
        qr_data = data.get('qr_data')
        course = get_object_or_404(Course, id=course_id)
        
        # Parse QR data (format: STUDENT:STUDENT_ID:MATRIC_NUMBER)
        if qr_data.startswith('STUDENT:'):
            parts = qr_data.split(':')
            if len(parts) >= 3:
                student_id = parts[1]
                matric_number = parts[2]
                
                try:
                    student = Student.objects.get(
                        student_id=student_id,
                        matric_number=matric_number,
                        department=course.department,
                        level=course.level
                    )
                    
                    # Mark attendance
                    attendance, created = Attendance.objects.get_or_create(
                        student=student,
                        course=course,
                        date=date.today(),
                        defaults={
                            'status': 'present',
                            'marked_by': request.user.lecturer_profile
                        }
                    )
                    
                    if not created:
                        attendance.status = 'present'
                        attendance.save()
                    
                    return JsonResponse({
                        'success': True,
                        'message': f'Attendance marked for {student.user.get_full_name()}',
                        'student_name': student.user.get_full_name(),
                        'matric_number': student.matric_number
                    })
                    
                except Student.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'message': 'Student not found or not enrolled in this course'
                    })
        
        return JsonResponse({
            'success': False,
            'message': 'Invalid QR code format'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

# Admin Management Views
@login_required
@user_passes_test(lambda u: is_admin(u) or is_super_admin(u))
def manage_courses(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course added successfully!')
            return redirect('manage_courses')
    else:
        form = CourseForm()
    
    courses = Course.objects.all().order_by('code')
    context = {
        'form': form,
        'courses': courses,
    }
    return render(request, 'core/manage_courses.html', context)

@login_required
@user_passes_test(lambda u: is_admin(u) or is_super_admin(u))
def manage_timetable(request):
    if request.method == 'POST':
        form = TimetableForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Timetable entry added successfully!')
            return redirect('manage_timetable')
    else:
        form = TimetableForm()
    
    timetable = Timetable.objects.all().order_by('day', 'start_time')
    context = {
        'form': form,
        'timetable': timetable,
    }
    return render(request, 'core/manage_timetable.html', context)

@login_required
@user_passes_test(lambda u: is_admin(u) or is_super_admin(u))
def manage_departments(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department added successfully!')
            return redirect('manage_departments')
    else:
        form = DepartmentForm()
    
    departments = Department.objects.all().order_by('name')
    context = {
        'form': form,
        'departments': departments,
    }
    return render(request, 'core/manage_departments.html', context)

@login_required
@user_passes_test(lambda u: is_admin(u) or is_super_admin(u))
def manage_levels(request):
    if request.method == 'POST':
        form = LevelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Level added successfully!')
            return redirect('manage_levels')
    else:
        form = LevelForm()
    
    levels = Level.objects.all().order_by('level_number')
    context = {
        'form': form,
        'levels': levels,
    }
    return render(request, 'core/manage_levels.html', context)

@login_required
@user_passes_test(lambda u: is_admin(u) or is_super_admin(u))
def manage_lecturers(request):
    if request.method == 'POST':
        form = LecturerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lecturer added successfully!')
            return redirect('manage_lecturers')
    else:
        form = LecturerForm()
    
    lecturers = Lecturer.objects.all().order_by('user__first_name')
    context = {
        'form': form,
        'lecturers': lecturers,
    }
    return render(request, 'core/manage_lecturers.html', context)

@login_required
@user_passes_test(is_super_admin)
def manage_admins(request):
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Administrator added successfully!')
            return redirect('manage_admins')
    else:
        form = AdminForm()
    
    admins = Admin.objects.all().order_by('user__first_name')
    context = {
        'form': form,
        'admins': admins,
    }
    return render(request, 'core/manage_admins.html', context)

@login_required
@user_passes_test(lambda u: is_admin(u) or is_super_admin(u))
def attendance_reports(request):
    department_id = request.GET.get('department')
    level_id = request.GET.get('level')
    course_id = request.GET.get('course')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    status_filter = request.GET.get('status')
    
    attendance_records = Attendance.objects.all()
    
    if department_id:
        attendance_records = attendance_records.filter(course__department_id=department_id)
    if level_id:
        attendance_records = attendance_records.filter(course__level_id=level_id)
    if course_id:
        attendance_records = attendance_records.filter(course_id=course_id)
    if date_from:
        attendance_records = attendance_records.filter(date__gte=date_from)
    if date_to:
        attendance_records = attendance_records.filter(date__lte=date_to)
    if status_filter:
        attendance_records = attendance_records.filter(status=status_filter)
    
    # Calculate statistics
    total_records = attendance_records.count()
    present_count = attendance_records.filter(status='present').count()
    absent_count = attendance_records.filter(status='absent').count()
    late_count = attendance_records.filter(status='late').count()
    
    attendance_records = attendance_records.order_by('-date', 'course__code')
    
    departments = Department.objects.all()
    levels = Level.objects.all()
    courses = Course.objects.all()
    
    context = {
        'attendance_records': attendance_records,
        'departments': departments,
        'levels': levels,
        'courses': courses,
        'total_records': total_records,
        'present_count': present_count,
        'absent_count': absent_count,
        'late_count': late_count,
        'filters': {
            'department_id': department_id,
            'level_id': level_id,
            'course_id': course_id,
            'date_from': date_from,
            'date_to': date_to,
            'status': status_filter,
        }
    }
    return render(request, 'core/attendance_reports.html', context)

def login_portal(request):
    return render(request, 'core/login_portal.html')
