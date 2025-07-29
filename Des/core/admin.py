from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_active')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type',)}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('user_type',)}),
    )

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    ordering = ('name',)

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'level_number')
    search_fields = ('name',)
    ordering = ('level_number',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'matric_number', 'student_id', 'department', 'level')
    list_filter = ('department', 'level')
    search_fields = ('user__first_name', 'user__last_name', 'matric_number', 'student_id')
    ordering = ('matric_number',)
    readonly_fields = ('student_id', 'qr_code')

@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'department')
    list_filter = ('department',)
    search_fields = ('user__first_name', 'user__last_name', 'employee_id')
    ordering = ('user__first_name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'department', 'level', 'lecturer', 'credit_units')
    list_filter = ('department', 'level', 'lecturer')
    search_fields = ('code', 'title', 'lecturer__user__first_name', 'lecturer__user__last_name')
    ordering = ('code',)

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('course', 'department', 'level', 'day', 'start_time', 'end_time')
    list_filter = ('department', 'level', 'day', 'course')
    search_fields = ('course__code', 'course__title')
    ordering = ('day', 'start_time')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'status', 'marked_by', 'marked_at')
    list_filter = ('status', 'date', 'course__department', 'course__level')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'student__matric_number', 'course__code')
    ordering = ('-date', 'course__code')
    readonly_fields = ('marked_at',)

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'admin_id', 'role')
    list_filter = ('role',)
    search_fields = ('user__first_name', 'user__last_name', 'admin_id')
    ordering = ('user__first_name',)
