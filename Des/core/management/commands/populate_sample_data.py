from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import *
from datetime import date, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Get existing departments
        departments = list(Department.objects.all())
        self.stdout.write(f'Using existing departments: {[d.name for d in departments]}')
        
        # Create levels
        levels = []
        for i in range(1, 6):
            level, created = Level.objects.get_or_create(
                level_number=i,
                defaults={'name': f'Level {i}'}
            )
            levels.append(level)
            if created:
                self.stdout.write(f'Created level: {i}')
            else:
                self.stdout.write(f'Level already exists: {i}')
        
        # Create super admin
        try:
            super_admin_user = User.objects.get(username='superadmin')
            self.stdout.write('Super admin already exists')
        except User.DoesNotExist:
            super_admin_user = User.objects.create_user(
                username='superadmin@university.com',
                email='superadmin@university.com',
                password='admin123',
                first_name='Super',
                last_name='Admin',
                user_type='super_admin',
                is_staff=True,
                is_superuser=True,
            )
            
            admin_profile, created = Admin.objects.get_or_create(
                user=super_admin_user,
                defaults={
                    'admin_id': 'SUPER001',
                    'role': 'super_admin'
                }
            )
            self.stdout.write('Created super admin')
        
        # Create regular admin
        try:
            admin_user = User.objects.get(username='admin')
            self.stdout.write('Regular admin already exists')
        except User.DoesNotExist:
            admin_user = User.objects.create_user(
                username='admin@university.com',
                email='admin@university.com',
                password='admin123',
                first_name='Regular',
                last_name='Admin',
                user_type='admin',
                is_staff=True,
            )
            
            admin_profile, created = Admin.objects.get_or_create(
                user=admin_user,
                defaults={
                    'admin_id': 'ADMIN001',
                    'role': 'admin'
                }
            )
            self.stdout.write('Created regular admin')
        
        # Create lecturers
        lecturers = []
        lecturer_data = [
            ('Dr. John Smith', 'LEC002', 'CS'),
            ('Prof. Sarah Johnson', 'LEC003', 'MATH'),
            ('Dr. Michael Brown', 'LEC004', 'EE'),
            ('Prof. Emily Davis', 'LEC005', 'ME'),
            ('Dr. Robert Wilson', 'LEC006', 'CE'),
        ]
        
        for name, emp_id, dept_code in lecturer_data:
            first_name, last_name = name.split(' ', 1)
            try:
                dept = Department.objects.get(code=dept_code)
            except Department.DoesNotExist:
                dept = departments[0]  # Use first available department
            
            try:
                lecturer_user = User.objects.get(username=f'{emp_id.lower()}@university.com')
                self.stdout.write(f'Lecturer already exists: {name}')
            except User.DoesNotExist:
                lecturer_user = User.objects.create_user(
                    username=f'{emp_id.lower()}@university.com',
                    email=f'{emp_id.lower()}@university.com',
                    password='lecturer123',
                    first_name=first_name,
                    last_name=last_name,
                    user_type='lecturer',
                )
                
                lecturer_profile, created = Lecturer.objects.get_or_create(
                    user=lecturer_user,
                    defaults={
                        'employee_id': emp_id,
                        'department': dept
                    }
                )
                lecturers.append(lecturer_profile)
                self.stdout.write(f'Created lecturer: {name}')
        
        # Create courses
        courses = []
        course_data = [
            ('Introduction to Computer Science', 'CSC101', 'CS', 1, 0),
            ('Programming Fundamentals', 'CSC102', 'CS', 1, 0),
            ('Data Structures', 'CSC201', 'CS', 2, 0),
            ('Calculus I', 'MTH101', 'MATH', 1, 1),
            ('Linear Algebra', 'MTH201', 'MATH', 2, 1),
            ('Electrical Circuits', 'EE101', 'EE', 1, 2),
            ('Mechanical Design', 'ME101', 'ME', 1, 3),
            ('Civil Engineering Basics', 'CE101', 'CE', 1, 4),
        ]
        
        for title, code, dept_code, level_num, lecturer_idx in course_data:
            try:
                dept = Department.objects.get(code=dept_code)
            except Department.DoesNotExist:
                dept = departments[0]  # Use first available department
            
            level = Level.objects.get(level_number=level_num)
            lecturer = lecturers[lecturer_idx] if lecturer_idx < len(lecturers) else lecturers[0]
            
            course, created = Course.objects.get_or_create(
                code=code,
                defaults={
                    'title': title,
                    'department': dept,
                    'level': level,
                    'lecturer': lecturer,
                    'credit_units': 3
                }
            )
            courses.append(course)
            if created:
                self.stdout.write(f'Created course: {code}')
        
        # Create students
        students = []
        student_names = [
            'Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Diana Prince', 'Eve Wilson',
            'Frank Miller', 'Grace Lee', 'Henry Davis', 'Ivy Chen', 'Jack Taylor',
            'Kate Anderson', 'Liam O\'Connor', 'Maya Patel', 'Noah Garcia', 'Olivia White',
            'Paul Rodriguez', 'Quinn Thompson', 'Ruby Martinez', 'Sam Johnson', 'Tina Kim'
        ]
        
        for i, full_name in enumerate(student_names):
            first_name, last_name = full_name.split(' ', 1)
            matric_number = f"CS/20/{1000 + i:04d}"
            email = f"{first_name.lower()}.{last_name.lower()}@student.university.com"
            
            student_user, created = User.objects.get_or_create(
                username=email,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'user_type': 'student',
                }
            )
            if created:
                student_user.set_password('student123')
                student_user.save()
                
                # Assign to CS department, level 1
                dept = Department.objects.get(code='CS')
                level = Level.objects.get(level_number=1)
                
                student_profile, created = Student.objects.get_or_create(
                    user=student_user,
                    defaults={
                        'matric_number': matric_number,
                        'department': dept,
                        'level': level
                    }
                )
                students.append(student_profile)
                self.stdout.write(f'Created student: {full_name}')
        
        # Create timetable entries
        timetable_data = [
            ('CS', 1, 'CSC101', 'monday', '08:00', '10:00'),
            ('CS', 1, 'CSC102', 'tuesday', '10:00', '12:00'),
            ('CS', 2, 'CSC201', 'wednesday', '14:00', '16:00'),
            ('MTH', 1, 'MTH101', 'monday', '10:00', '12:00'),
            ('MTH', 2, 'MTH201', 'tuesday', '14:00', '16:00'),
            ('PHY', 1, 'PHY101', 'thursday', '08:00', '10:00'),
            ('CHE', 1, 'CHE101', 'friday', '10:00', '12:00'),
            ('BIO', 1, 'BIO101', 'wednesday', '10:00', '12:00'),
        ]
        
        for dept_code, level_num, course_code, day, start_time, end_time in timetable_data:
            dept = Department.objects.get(code=dept_code)
            level = Level.objects.get(level_number=level_num)
            course = Course.objects.get(code=course_code)
            
            timetable, created = Timetable.objects.get_or_create(
                department=dept,
                level=level,
                course=course,
                day=day,
                defaults={
                    'start_time': start_time,
                    'end_time': end_time
                }
            )
            if created:
                self.stdout.write(f'Created timetable: {course_code} on {day}')
        
        # Create sample attendance records
        # Get the first course for sample attendance
        sample_course = Course.objects.first()
        if sample_course and students:
            # Create attendance for the last 7 days
            for i in range(7):
                attendance_date = date.today() - timedelta(days=i)
                
                for student in students[:10]:  # First 10 students
                    status = random.choice(['present', 'absent', 'late'])
                    
                    attendance, created = Attendance.objects.get_or_create(
                        student=student,
                        course=sample_course,
                        date=attendance_date,
                        defaults={
                            'status': status,
                            'marked_by': lecturers[0],
                            'notes': f'Sample attendance for {attendance_date}'
                        }
                    )
                    if created:
                        self.stdout.write(f'Created attendance: {student.user.get_full_name()} - {status}')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write('\nLogin Credentials:')
        self.stdout.write('Super Admin: superadmin@university.com / admin123')
        self.stdout.write('Admin: admin@university.com / admin123')
        self.stdout.write('Lecturer: lec001@university.com / lecturer123')
        self.stdout.write('Student: alice.johnson@student.university.com / student123')