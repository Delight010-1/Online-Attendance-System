from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
import uuid

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('admin', 'Admin'),
        ('super_admin', 'Super Admin'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.username} - {self.user_type}"

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    class Meta:
        ordering = ['name']

class Level(models.Model):
    name = models.CharField(max_length=50, unique=True)
    level_number = models.IntegerField(unique=True)
    
    def __str__(self):
        return f"Level {self.level_number} - {self.name}"
    
    class Meta:
        ordering = ['level_number']

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    matric_number = models.CharField(max_length=20, unique=True, validators=[
        RegexValidator(regex=r'^[A-Z]{2,3}/\d{2}/\d{4}$', message='Matric number must be in format: CS/20/1234')
    ])
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    student_id = models.CharField(max_length=20, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.student_id:
            self.student_id = f"STU{str(uuid.uuid4())[:8].upper()}"
        if not self.qr_code:
            self.generate_qr_code()
        super().save(*args, **kwargs)
    
    def generate_qr_code(self):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f"STUDENT:{self.student_id}:{self.matric_number}")
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        
        filename = f'qr_code_{self.student_id}.png'
        self.qr_code.save(filename, File(buffer), save=False)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.matric_number}"
    
    class Meta:
        ordering = ['matric_number']

class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lecturer_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.employee_id}"
    
    class Meta:
        ordering = ['user__first_name']

class Course(models.Model):
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    credit_units = models.IntegerField(default=3)
    
    def __str__(self):
        return f"{self.code} - {self.title}"
    
    class Meta:
        ordering = ['code']

class Timetable(models.Model):
    DAY_CHOICES = (
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    )
    
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return f"{self.course.code} - {self.day} {self.start_time}-{self.end_time}"
    
    class Meta:
        ordering = ['day', 'start_time']
        unique_together = ['department', 'level', 'course', 'day']

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='absent')
    marked_by = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    marked_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.student.matric_number} - {self.course.code} - {self.date} - {self.status}"
    
    class Meta:
        ordering = ['-date', 'student__matric_number']
        unique_together = ['student', 'course', 'date']

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    admin_id = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=[
        ('admin', 'Admin'),
        ('super_admin', 'Super Admin'),
    ], default='admin')
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role}"
    
    class Meta:
        ordering = ['user__first_name']
