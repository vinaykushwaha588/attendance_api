from rest_framework import viewsets
from rest_framework.views import Response
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    @action(detail=False, methods=['post'])
    def register(self, request):
        try:
            data = request.data.copy()
            serializer = UserSerializers(data=data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                user.set_password(serializer.validated_data['password'])
                user.save()
                return Response({'success': True, 'message': "User Created Successfully."},
                                status=status.HTTP_201_CREATED)
            return Response({'success': False, 'message': serializer.error_messages},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'success': False, 'error': err.args[0]})

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        try:
            data = request.data.copy()
            email = data.get('email', None)
            password = data.get('password', None)
            user = authenticate(request, username=email, password=password)

            if not user:
                raise AuthenticationFailed('Invalid Credentials.')

            if user is not None:
                return Response({
                    'access': user.tokens()['access'],
                    'refresh': user.tokens()['refresh'],
                }, status=status.HTTP_200_OK)

            return Response({'success': False, 'message': "Invalid Credentials."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({"success": False, 'error': err.args[0]})

    @action(detail=False, methods=['get'])
    def user_list(self, request):
        queryset = User.objects.all().values('id', 'name', 'email', 'mobile', 'created_at', 'updated_at')
        return Response({'success': True, 'data': queryset}, status=status.HTTP_200_OK)


class DepartmentListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            if not request.user.is_staff:
                return Response({'detail': 'You do not have permission to perform this action.'},
                                status=status.HTTP_403_FORBIDDEN)
            serializer = DepartmentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"success": True, 'message': "department created successfully."},
                                status=status.HTTP_201_CREATED)
            return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'detail': err.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CourseListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            if not request.user.is_staff:
                return Response({'detail': 'You do not have permission to perform this action.'},
                                status=status.HTTP_403_FORBIDDEN)
            serializer = CourseSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(submitted_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'detail': err.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = StudentSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(submitted_by=request.user)
                return Response({'success': True, 'message': 'Student Details created Successfully.'},
                                status=status.HTTP_201_CREATED)
            return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'detail': err.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AttendanceListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        attendances = Attendance.objects.all()
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = AttendanceSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(submitted_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'detail': err.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

