from rest_framework import serializers
from .models import *


class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data['email'],
                    full_name=validated_data['full_name'], type=validated_data['type'])
        return user

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name', 'submitted_by', 'updated_at']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'department', 'semester', 'class_name', 'lecture_hours', 'submitted_by',
                  'updated_at']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'full_name', 'department', 'class_name', 'submitted_by', 'updated_at']


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'student', 'course', 'present', 'submitted_by', 'updated_at']
