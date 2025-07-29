from django.urls import path
from . import views

urlpatterns = [
    # Home and Authentication
    path('', views.home, name='home'),
    path('student/register/', views.student_register, name='student_register'),
    path('student/login/', views.student_login, name='student_login'),
    path('lecturer/login/', views.lecturer_login, name='lecturer_login'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboards
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('lecturer/dashboard/', views.lecturer_dashboard, name='lecturer_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('super-admin/dashboard/', views.super_admin_dashboard, name='super_admin_dashboard'),
    
    # Student Views
    path('student/qr-code/', views.student_qr_code, name='student_qr_code'),
    path('student/attendance-history/', views.attendance_history, name='attendance_history'),
    path('student/timetable/', views.timetable_view, name='timetable_view'),
    
    # Lecturer Views
    path('lecturer/mark-attendance/<int:course_id>/', views.mark_attendance, name='mark_attendance'),
    path('lecturer/qr-scanner/<int:course_id>/', views.qr_scanner, name='qr_scanner'),
    path('lecturer/process-qr/<int:course_id>/', views.process_qr_scan, name='process_qr_scan'),
    
    # Admin Management Views
    path('admin/manage/courses/', views.manage_courses, name='manage_courses'),
    path('admin/manage/timetable/', views.manage_timetable, name='manage_timetable'),
    path('admin/manage/departments/', views.manage_departments, name='manage_departments'),
    path('admin/manage/levels/', views.manage_levels, name='manage_levels'),
    path('admin/manage/lecturers/', views.manage_lecturers, name='manage_lecturers'),
    path('admin/manage/admins/', views.manage_admins, name='manage_admins'),
    path('admin/reports/', views.attendance_reports, name='attendance_reports'),
] 