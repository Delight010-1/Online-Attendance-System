from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import User, Student, Lecturer, Course, Department, Level, Timetable, Attendance

class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    matric_number = forms.CharField(max_length=20, required=True)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)
    level = forms.ModelChoiceField(queryset=Level.objects.all(), required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'matric_number', 'department', 'level', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'student'
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            student = Student.objects.create(
                user=user,
                matric_number=self.cleaned_data['matric_number'],
                department=self.cleaned_data['department'],
                level=self.cleaned_data['level']
            )
        return user

class LecturerLoginForm(AuthenticationForm):
    username = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            # Try to find lecturer by name
            try:
                lecturer = Lecturer.objects.get(user__first_name__icontains=username)
                user = authenticate(username=lecturer.user.username, password=password)
                if user is None:
                    raise forms.ValidationError('Invalid credentials')
                self.user_cache = user
            except Lecturer.DoesNotExist:
                raise forms.ValidationError('Lecturer not found')
        
        return self.cleaned_data

class AdminLoginForm(AuthenticationForm):
    username = forms.CharField(label='User ID', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            # Try to find admin by admin_id
            try:
                admin = Admin.objects.get(admin_id=username)
                user = authenticate(username=admin.user.username, password=password)
                if user is None:
                    raise forms.ValidationError('Invalid credentials')
                self.user_cache = user
            except Admin.DoesNotExist:
                raise forms.ValidationError('Admin not found')
        
        return self.cleaned_data

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'code', 'department', 'level', 'lecturer', 'credit_units']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'lecturer': forms.Select(attrs={'class': 'form-control'}),
            'credit_units': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['department', 'level', 'course', 'day', 'start_time', 'end_time']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'day': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['status', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = ['name', 'level_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'level_number': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class LecturerForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    
    class Meta:
        model = Lecturer
        fields = ['employee_id', 'department']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def save(self, commit=True):
        lecturer = super().save(commit=False)
        
        # Create user account
        user = User.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            user_type='lecturer'
        )
        
        lecturer.user = user
        
        if commit:
            lecturer.save()
        
        return lecturer 