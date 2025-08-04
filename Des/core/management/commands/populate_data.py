from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
import random

from core.models import (
    Department, Level, Student, Lecturer, Course, 
    Timetable, Attendance, Admin
)

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database with sample data for demonstration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            self.clear_data()

        self.stdout.write(self.style.SUCCESS('Starting data population...'))
        
        # Create departments
        departments = self.create_departments()
        self.stdout.write(self.style.SUCCESS(f'Created {len(departments)} departments'))
        
        # Create levels
        levels = self.create_levels()
        self.stdout.write(self.style.SUCCESS(f'Created {len(levels)} levels'))
        
        # Create admin users
        admins = self.create_admins()
        self.stdout.write(self.style.SUCCESS(f'Created {len(admins)} admin users'))
        
        # Create lecturers
        lecturers = self.create_lecturers(departments)
        self.stdout.write(self.style.SUCCESS(f'Created {len(lecturers)} lecturers'))
        
        # Create courses
        courses = self.create_courses(departments, levels, lecturers)
        self.stdout.write(self.style.SUCCESS(f'Created {len(courses)} courses'))
        
        # Create timetables
        timetables = self.create_timetables(departments, levels, courses)
        self.stdout.write(self.style.SUCCESS(f'Created {len(timetables)} timetable entries'))
        
        # Create students
        students = self.create_students(departments, levels)
        self.stdout.write(self.style.SUCCESS(f'Created {len(students)} students'))
        
        # Create attendance records
        attendance_records = self.create_attendance_records(students, courses, lecturers)
        self.stdout.write(self.style.SUCCESS(f'Created {len(attendance_records)} attendance records'))
        
        self.stdout.write(self.style.SUCCESS('Data population completed successfully!'))

    def clear_data(self):
        """Clear existing data"""
        Attendance.objects.all().delete()
        Timetable.objects.all().delete()
        Course.objects.all().delete()
        Student.objects.all().delete()
        Lecturer.objects.all().delete()
        Admin.objects.all().delete()
        Level.objects.all().delete()
        Department.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

    def create_departments(self):
        """Create sample departments"""
        dept_data = [
            {'name': 'Computer Science', 'code': 'CS'},
            {'name': 'Mathematics', 'code': 'MATH'},
            {'name': 'Physics', 'code': 'PHY'},
            {'name': 'Chemistry', 'code': 'CHEM'},
            {'name': 'Biology', 'code': 'BIO'},
            {'name': 'Engineering', 'code': 'ENG'},
        ]
        
        departments = []
        for data in dept_data:
            dept, created = Department.objects.get_or_create(
                code=data['code'],
                defaults={'name': data['name']}
            )
            departments.append(dept)
        
        return departments

    def create_levels(self):
        """Create academic levels"""
        level_data = [
            {'name': 'First Year', 'level_number': 100},
            {'name': 'Second Year', 'level_number': 200},
            {'name': 'Third Year', 'level_number': 300},
            {'name': 'Fourth Year', 'level_number': 400},
        ]
        
        levels = []
        for data in level_data:
            level, created = Level.objects.get_or_create(
                level_number=data['level_number'],
                defaults={'name': data['name']}
            )
            levels.append(level)
        
        return levels

    def create_admins(self):
        """Create admin users"""
        admin_data = [
            {
                'first_name': 'Super', 'last_name': 'Admin',
                'email': 'superadmin@university.edu',
                'username': 'superadmin@university.edu',
                'admin_id': 'SUPER001',
                'role': 'super_admin'
            },
            {
                'first_name': 'John', 'last_name': 'Admin',
                'email': 'admin@university.edu',
                'username': 'admin@university.edu',
                'admin_id': 'ADMIN001',
                'role': 'admin'
            },
        ]
        
        admins = []
        for data in admin_data:
            user, created = User.objects.get_or_create(
                email=data['email'],
                defaults={
                    'username': data['username'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'user_type': data['role'],
                    'is_staff': True,
                    'is_active': True,
                }
            )
            if created:
                user.set_password('admin123')
                user.save()
            
            admin, created = Admin.objects.get_or_create(
                user=user,
                defaults={
                    'admin_id': data['admin_id'],
                    'role': data['role']
                }
            )
            admins.append(admin)
        
        return admins

    def create_lecturers(self, departments):
        """Create sample lecturers"""
        lecturer_data = [
            {'first_name': 'Dr. Alice', 'last_name': 'Johnson', 'email': 'alice.johnson@university.edu', 'employee_id': 'EMP001'},
            {'first_name': 'Prof. Bob', 'last_name': 'Smith', 'email': 'bob.smith@university.edu', 'employee_id': 'EMP002'},
            {'first_name': 'Dr. Carol', 'last_name': 'Williams', 'email': 'carol.williams@university.edu', 'employee_id': 'EMP003'},
            {'first_name': 'Prof. David', 'last_name': 'Brown', 'email': 'david.brown@university.edu', 'employee_id': 'EMP004'},
            {'first_name': 'Dr. Eve', 'last_name': 'Davis', 'email': 'eve.davis@university.edu', 'employee_id': 'EMP005'},
            {'first_name': 'Prof. Frank', 'last_name': 'Miller', 'email': 'frank.miller@university.edu', 'employee_id': 'EMP006'},
        ]
        
        lecturers = []
        for i, data in enumerate(lecturer_data):
            user, created = User.objects.get_or_create(
                email=data['email'],
                defaults={
                    'username': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'user_type': 'lecturer',
                    'is_active': True,
                }
            )
            if created:
                user.set_password('lecturer123')
                user.save()
            
            lecturer, created = Lecturer.objects.get_or_create(
                user=user,
                defaults={
                    'employee_id': data['employee_id'],
                    'department': departments[i % len(departments)]
                }
            )
            lecturers.append(lecturer)
        
        return lecturers

    def create_courses(self, departments, levels, lecturers):
        """Create sample courses"""
        course_data = [
            # Computer Science courses
            {'title': 'Introduction to Programming', 'code': 'CS101', 'dept_idx': 0, 'level_idx': 0, 'credit_units': 3},
            {'title': 'Data Structures', 'code': 'CS201', 'dept_idx': 0, 'level_idx': 1, 'credit_units': 3},
            {'title': 'Algorithms', 'code': 'CS301', 'dept_idx': 0, 'level_idx': 2, 'credit_units': 4},
            {'title': 'Software Engineering', 'code': 'CS401', 'dept_idx': 0, 'level_idx': 3, 'credit_units': 3},
            
            # Mathematics courses
            {'title': 'Calculus I', 'code': 'MATH101', 'dept_idx': 1, 'level_idx': 0, 'credit_units': 3},
            {'title': 'Linear Algebra', 'code': 'MATH201', 'dept_idx': 1, 'level_idx': 1, 'credit_units': 3},
            {'title': 'Statistics', 'code': 'MATH301', 'dept_idx': 1, 'level_idx': 2, 'credit_units': 3},
            
            # Physics courses
            {'title': 'General Physics I', 'code': 'PHY101', 'dept_idx': 2, 'level_idx': 0, 'credit_units': 4},
            {'title': 'Thermodynamics', 'code': 'PHY201', 'dept_idx': 2, 'level_idx': 1, 'credit_units': 3},
            
            # Chemistry courses
            {'title': 'General Chemistry', 'code': 'CHEM101', 'dept_idx': 3, 'level_idx': 0, 'credit_units': 4},
            {'title': 'Organic Chemistry', 'code': 'CHEM201', 'dept_idx': 3, 'level_idx': 1, 'credit_units': 4},
        ]
        
        courses = []
        for data in course_data:
            course, created = Course.objects.get_or_create(
                code=data['code'],
                defaults={
                    'title': data['title'],
                    'department': departments[data['dept_idx']],
                    'level': levels[data['level_idx']],
                    'lecturer': lecturers[random.randint(0, len(lecturers)-1)],
                    'credit_units': data['credit_units']
                }
            )
            courses.append(course)
        
        return courses

    def create_timetables(self, departments, levels, courses):
        """Create sample timetables"""
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        times = [
            ('08:00', '10:00'),
            ('10:00', '12:00'),
            ('12:00', '14:00'),
            ('14:00', '16:00'),
            ('16:00', '18:00'),
        ]
        
        timetables = []
        for course in courses:
            day = random.choice(days)
            start_time, end_time = random.choice(times)
            
            timetable, created = Timetable.objects.get_or_create(
                department=course.department,
                level=course.level,
                course=course,
                day=day,
                defaults={
                    'start_time': start_time,
                    'end_time': end_time
                }
            )
            if created:
                timetables.append(timetable)
        
        return timetables

    def create_students(self, departments, levels):
        """Create sample students"""
        first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'James', 'Jessica', 'Robert', 'Ashley']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
        
        students = []
        student_count = 50
        
        for i in range(student_count):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            department = random.choice(departments)
            level = random.choice(levels)
            
            # Generate matric number
            year = random.choice(['22', '23', '24'])
            matric_number = f"{department.code}/{year}/{1000 + i:04d}"
            email = f"{first_name.lower()}.{last_name.lower()}{i}@student.university.edu"
            
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'user_type': 'student',
                    'is_active': True,
                }
            )
            if created:
                user.set_password('student123')
                user.save()
            
            student, created = Student.objects.get_or_create(
                matric_number=matric_number,
                defaults={
                    'user': user,
                    'department': department,
                    'level': level
                }
            )
            if created:
                students.append(student)
        
        return students

    def create_attendance_records(self, students, courses, lecturers):
        """Create sample attendance records"""
        attendance_records = []
        
        # Create records for the last 30 days
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)
        
        current_date = start_date
        while current_date <= end_date:
            # Skip weekends
            if current_date.weekday() < 5:  # Monday = 0, Friday = 4
                # Randomly select some courses for today
                daily_courses = random.sample(courses, min(3, len(courses)))
                
                for course in daily_courses:
                    # Get students for this course's department and level
                    course_students = [
                        s for s in students 
                        if s.department == course.department and s.level == course.level
                    ]
                    
                    if course_students:
                        # Randomly mark attendance for some students
                        present_students = random.sample(
                            course_students,
                            min(random.randint(5, 15), len(course_students))
                        )
                        
                        for student in present_students:
                            status = random.choices(
                                ['present', 'late', 'absent'],
                                weights=[70, 20, 10]
                            )[0]
                            
                            attendance, created = Attendance.objects.get_or_create(
                                student=student,
                                course=course,
                                date=current_date,
                                defaults={
                                    'status': status,
                                    'marked_by': course.lecturer,
                                    'notes': random.choice(['', 'Good participation', 'Late due to traffic', '']) if status != 'absent' else ''
                                }
                            )
                            if created:
                                attendance_records.append(attendance)
            
            current_date += timedelta(days=1)
        
        return attendance_records