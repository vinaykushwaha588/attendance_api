from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.core.validators import validate_email
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import models

name_validator = RegexValidator(r'^[a-zA-Z ]+$', 'Only alphabetic characters are allowed.')


class UserManager(BaseUserManager):
    def create_user(self, email, password, full_name=None, **extra_fields):
        if not email:
            raise ValueError("Email id required!")

        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True!')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True!')

        return self.create_user(email, password, **extra_fields)


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = (
        ('student', "Student"),
        ('teacher', "Teacher"),
        ('admin', "Admin"),

    )
    type = models.CharField(choices=USER_TYPE, max_length=50, null=True)
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, validators=[name_validator])
    email = models.EmailField(unique=True, validators=[validate_email])
    submitted_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'username']
    objects = UserManager()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class Department(models.Model):
    department_name = models.CharField(max_length=100)
    submitted_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.department_name


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.IntegerField()
    class_name = models.CharField(max_length=100)
    lecture_hours = models.IntegerField()
    submitted_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.course_name


class Student(models.Model):
    full_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=100)
    submitted_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)
    submitted_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.course.course_name} - {'Present' if self.present else 'Absent'}"
