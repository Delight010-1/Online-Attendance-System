from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import *

User = get_user_model()

class Command(BaseCommand):
    help = 'Set up initial data for the attendance system'

    def handle(self, *args, **options):
        self.stdout.write('Setting up initial data...')
        
        # Create departments
        departments = [
            {'name': 'Computer Science', 'code': 'CS'},
            {'name': 'Electrical Engineering', 'code': 'EE'},
            {'name': 'Mechanical Engineering', 'code': 'ME'},
            {'name': 'Civil Engineering', 'code': 'CE'},
            {'name': 'Mathematics', 'code': 'MATH'},
        ]
        
        for dept_data in departments:
            dept, created = Department.objects.get_or_create(
                code=dept_data['code'],
                defaults={'name': dept_data['name']}
            )
            if created:
                self.stdout.write(f'Created department: {dept.name}')
        
        # Create levels
        levels = [
            {'name': 'First Year', 'level_number': 100},
            {'name': 'Second Year', 'level_number': 200},
            {'name': 'Third Year', 'level_number': 300},
            {'name': 'Fourth Year', 'level_number': 400},
        ]
        
        for level_data in levels:
            level, created = Level.objects.get_or_create(
                level_number=level_data['level_number'],
                defaults={'name': level_data['name']}
            )
            if created:
                self.stdout.write(f'Created level: {level.name}')
        
        # Create super admin
        super_admin_user, created = User.objects.get_or_create(
            username='superadmin',
            defaults={
                'email': 'superadmin@university.com',
                'first_name': 'Super',
                'last_name': 'Admin',
                'user_type': 'super_admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        
        if created:
            super_admin_user.set_password('admin123')
            super_admin_user.save()
            
            admin_profile, created = Admin.objects.get_or_create(
                user=super_admin_user,
                defaults={
                    'admin_id': 'SUPER001',
                    'role': 'super_admin'
                }
            )
            self.stdout.write('Created super admin user')
        
        # Create sample lecturer
        lecturer_user, created = User.objects.get_or_create(
            username='lecturer1',
            defaults={
                'email': 'lecturer1@university.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'user_type': 'lecturer',
            }
        )
        
        if created:
            lecturer_user.set_password('lecturer123')
            lecturer_user.save()
            
            lecturer_profile, created = Lecturer.objects.get_or_create(
                user=lecturer_user,
                defaults={
                    'employee_id': 'LEC001',
                    'department': Department.objects.get(code='CS')
                }
            )
            self.stdout.write('Created sample lecturer')
        
        # Create sample courses
        cs_dept = Department.objects.get(code='CS')
        level_100 = Level.objects.get(level_number=100)
        lecturer = Lecturer.objects.get(employee_id='LEC001')
        
        courses = [
            {
                'title': 'Introduction to Computer Science',
                'code': 'CSC101',
                'department': cs_dept,
                'level': level_100,
                'lecturer': lecturer,
                'credit_units': 3
            },
            {
                'title': 'Programming Fundamentals',
                'code': 'CSC102',
                'department': cs_dept,
                'level': level_100,
                'lecturer': lecturer,
                'credit_units': 4
            },
        ]
        
        for course_data in courses:
            course, created = Course.objects.get_or_create(
                code=course_data['code'],
                defaults=course_data
            )
            if created:
                self.stdout.write(f'Created course: {course.code}')
        
        # Create sample timetable
        timetable_entries = [
            {
                'department': cs_dept,
                'level': level_100,
                'course': Course.objects.get(code='CSC101'),
                'day': 'monday',
                'start_time': '08:00',
                'end_time': '10:00'
            },
            {
                'department': cs_dept,
                'level': level_100,
                'course': Course.objects.get(code='CSC102'),
                'day': 'wednesday',
                'start_time': '10:00',
                'end_time': '12:00'
            },
        ]
        
        for entry_data in timetable_entries:
            entry, created = Timetable.objects.get_or_create(
                department=entry_data['department'],
                level=entry_data['level'],
                course=entry_data['course'],
                day=entry_data['day'],
                defaults={
                    'start_time': entry_data['start_time'],
                    'end_time': entry_data['end_time']
                }
            )
            if created:
                self.stdout.write(f'Created timetable entry: {entry.course.code} on {entry.day}')
        
        self.stdout.write(self.style.SUCCESS('Initial data setup completed successfully!'))
        self.stdout.write('Super Admin - Username: superadmin, Password: admin123')
        self.stdout.write('Sample Lecturer - Username: lecturer1, Password: lecturer123') 