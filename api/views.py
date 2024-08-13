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
        def get(self, request, *args, **kwargs):
            """
            Handle GET requests to retrieve a list of departments.

            This method retrieves all the departments available in the database and returns them in a serialized format.

            Returns:
                Response: A JSON response containing a list of departments.

            Example:
                GET /departments/

                Response:
                [
                       {
                        "id": 1,
                        "department_name": "Computer Science",
                        "submitted_by": 5,
                        "updated_at": "2024-08-13T10:20:35.071412+05:30"
                        },
                        {
                            "id": 2,
                            "department_name": "Electorics and Communications",
                            "submitted_by": 5,
                            "updated_at": "2024-08-13T10:20:27.993879+05:30"
                        }
                    ...
                ]
            """
            departments = Department.objects.all()
            serializer = DepartmentSerializer(departments, many=True)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to create a new department.

        This method allows staff members to create a new department by providing the necessary data.

        Payload:
            department_name (str): The name of the department to be created. This field is required.

        Returns:
            Response: A JSON response indicating the success or failure of the department creation process.

        Raises:
            HTTP_403_FORBIDDEN: If the user does not have staff permissions.
            HTTP_400_BAD_REQUEST: If the provided data is invalid.
            HTTP_500_INTERNAL_SERVER_ERROR: If an unexpected error occurs during processing.

        Example:
            POST /departments/
            {
                "department_name": "Engineering"
            }
        """
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
        """
        Handle GET requests to retrieve a list of courses.

        This method retrieves all the courses available in the database and returns them in a serialized format.

        Returns:
            Response: A JSON response containing a list of courses with a success status.

        Response Structure:
            success (bool): Indicates if the request was successful.
            data (list): A list of serialized course objects.

        Example:
            GET /courses/

            Response:
            {
                "success": True,
                "data": [
                           {
            "id": 1,
            "course_name": "MCA",
            "department": 1,
            "semester": 2,
            "class_name": "MCA",
            "lecture_hours": 2,
            "submitted_by": 5,
            "updated_at": "2024-08-13T10:21:01.274318+05:30"
        },
        {
            "id": 2,
            "course_name": "Algorithms",
            "department": 2,
            "semester": 4,
            "class_name": "CS201",
            "lecture_hours": 50,
            "submitted_by": 5,
            "updated_at": "2024-08-13T10:20:56.407644+05:30"
        }
                    ...
                ]
            }
        """
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response({"success": True, 'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
         Handle POST requests to create a new course.

         This method allows staff members to create a new course by providing the necessary data.

         Payload:
             course_name (str): The name of the course. This field is required.
             department (str): The department associated with the course. This field is required.
             semester (int): The semester in which the course is offered. This field is required.
             class_name (str): The name of the class for the course. This field is required.
             lecture_hours (int): The number of lecture hours per week. This field is required.

         Returns:
             Response: A JSON response with the created course data or validation errors.

         Raises:
             HTTP_403_FORBIDDEN: If the user does not have staff permissions.
             HTTP_400_BAD_REQUEST: If the provided data is invalid.
             HTTP_500_INTERNAL_SERVER_ERROR: If an unexpected error occurs during processing.
        Example:
        POST /courses/
        {
            "course_name": "Advanced Python",
            "department": "Computer Science",
            "semester": 3,
            "class_name": "CS301",
            "lecture_hours": 3
        }

        Response:
        {
            "success": True,
            "message": "Course Created Successfully."
        }
        """
        try:
            if not request.user.is_staff:
                return Response({'detail': 'You do not have permission to perform this action.'},
                                status=status.HTTP_403_FORBIDDEN)
            serializer = CourseSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(submitted_by=request.user)
                return Response({'success': True, 'message': "Course Created Successfully."},
                                status=status.HTTP_201_CREATED)
            return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'detail': err.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
            Handle GET requests to retrieve a list of students.

            This method retrieves all the students from the database and returns their details in a serialized format.

            Returns:
                Response: A JSON response containing a list of student details with a success status.

            Response Structure:
                success (bool): Indicates if the request was successful.
                data (list): A list of serialized student objects.

            Example:
                GET /students/

                Response:
                {
                    "success": True,
                    "data": [
                               {
                                "id": 1,
                                "full_name": "Vinay Kushwaha",
                                "department": 1,
                                "class_name": "MCA",
                                "submitted_by": 5,
                                "updated_at": "2024-08-13T10:20:48.383134+05:30"
                                },
                                {
                                    "id": 2,
                                    "full_name": "Sintu Rana",
                                    "department": 2,
                                    "class_name": "B2",
                                    "submitted_by": 5,
                                    "updated_at": "2024-08-13T10:20:43.225388+05:30"
                                }
                        ...
                    ]
                }
            """

        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
            Handle POST requests to create a new student.

            This method allows the creation of a new student by providing the necessary details.

            Payload:
                full_name (str): The full name of the student. This field is required.
                department_id (int): The ID of the department to which the student belongs. This field is required.
                class_name (str): The name of the class the student is enrolled in. This field is required.

            Returns:
                Response: A JSON response indicating the success or failure of the student creation process.

            Response Structure:
                success (bool): Indicates if the student creation was successful.
                message (str): A message describing the result of the request.

            Raises:
                HTTP_400_BAD_REQUEST: If the provided data is invalid.
                HTTP_500_INTERNAL_SERVER_ERROR: If an unexpected error occurs during processing.

            Example:
                POST /students/
                {
                    "full_name": "Alice Johnson",
                    "department": 3,
                    "class_name": "Biology 101"
                }

                Response:
                {
                    "success": True,
                    "message": "Student Details created Successfully."
                }
            """
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
        """
            Handle GET requests to retrieve a list of attendance records.

            This method retrieves all attendance records from the database and returns them in a serialized format.

            Returns:
                Response: A JSON response containing a list of attendance records with a success status.

            Response Structure:
                success (bool): Indicates if the request was successful.
                data (list): A list of serialized attendance objects.

            Each attendance record in the list includes:
                id (int): The unique identifier for the attendance record.
                student (int): The ID of the student associated with the attendance record.
                course (int): The ID of the course associated with the attendance record.
                present (bool): Indicates whether the student was present (true) or absent (false).
                submitted_by (int): The ID of the user who submitted the attendance record.
                updated_at (str): The timestamp when the record was last updated (ISO 8601 format).

            Example:
                GET /attendance/

                Response:
                {
                    "success": True,
                    "data": [
                        {
                            "id": 1,
                            "student": 1,
                            "course": 1,
                            "present": true,
                            "submitted_by": 5,
                            "updated_at": "2024-08-13T10:21:15.207029+05:30"
                        },
                        {
                            "id": 2,
                            "student": 2,
                            "course": 2,
                            "present": true,
                            "submitted_by": 5,
                            "updated_at": "2024-08-13T10:21:07.479514+05:30"
                        }
                    ]
                }
            """

        attendances = Attendance.objects.all()
        serializer = AttendanceSerializer(attendances, many=True)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
            Handle POST requests to register student attendance.

            This method allows the registration of attendance for a student by providing the necessary details.

            Payload:
                student_id (int): The ID of the student whose attendance is being registered. This field is required.
                course_id (int): The ID of the course for which the attendance is being registered. This field is required.
                present (bool): Indicates whether the student was present (true) or absent (false). This field is required.

            Returns:
                Response: A JSON response indicating the success or failure of the attendance registration process.

            Response Structure:
                success (bool): Indicates if the attendance registration was successful.
                message (str): A message describing the result of the request.

            Raises:
                HTTP_400_BAD_REQUEST: If the provided data is invalid.
                HTTP_500_INTERNAL_SERVER_ERROR: If an unexpected error occurs during processing.

            Example:
                POST /attendance/
                {
                    "student_id": 1,
                    "course_id": 1,
                    "present": true
                }

                Response:
                {
                    "success": True,
                    "message": "Student Attendance has been registered."
                }
            """

        try:
            serializer = AttendanceSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(submitted_by=request.user)
                return Response({'success': True, 'message': "Student Attendance has been register."},
                                status=status.HTTP_201_CREATED)
            return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'detail': err.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
