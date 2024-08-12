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
        """
            Handle user registration.

            **Payload:**
            - `username` (str): The desired username for the new user.
            - `email` (str): The email address of the new user.
            - `full_name` (str): The full name of the new user.
            - `type` (str): The type of user (e.g., 'admin', 'teacher', 'student').
            - `password` (str): The password for the new user.

            **Response:**
            - On success:
              - HTTP 201 Created
              - JSON response: `{'success': True, 'message': "User Created Successfully."}`
            - On failure:
              - HTTP 400 Bad Request
              - JSON response: `{'success': False, 'message': <error messages>}`

            **Error Handling:**
            - If the payload is invalid or missing required fields, a 400 Bad Request error is returned with details of the validation errors.
            - Any other exceptions will result in a 500 Internal Server Error with the error message.

            Args:
                request (Request): The request object containing the user registration data.

            Returns:
                Response: The HTTP response object with the result of the registration attempt.
            """
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
        """
            Handles user login by authenticating the user with the provided email and password.

            Parameters:
            - request (Request): The request object containing the login data.
              Must include the following fields:
              - email (str): The email address of the user. Required.
              - password (str): The password of the user. Required.

            Returns:
            - Response: A Response object with the following possible outcomes:
              - If authentication is successful:
                - Status code: 200 OK
                - Body:
                  - access (str): The access token for the user.
                  - refresh (str): The refresh token for the user.
              - If authentication fails:
                - Status code: 400 Bad Request
                - Body:
                  - success (bool): False
                  - message (str): "Invalid Credentials."
              - If an unexpected error occurs:
                - Status code: 500 Internal Server Error
                - Body:
                  - success (bool): False
                  - error (str): Description of the error.

            Raises:
            - AuthenticationFailed: If the provided email and password do not match any user.
            """

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
        queryset = User.objects.all()
        serializer = UserSerializers(queryset, many=True).data
        return Response({'success': True, 'data': serializer}, status=status.HTTP_200_OK)


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
