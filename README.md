Attendance Management System
## Overview

This is an Attendance Management System built using Django and Django REST Framework. The system provides functionalities for managing student attendance, courses, and departments. It includes APIs for creating, retrieving, and updating records.

## Features
- - **User Authentication**: Implemented login and signup functionalities.
- **Student Management**: Create and retrieve student details.
- **Course Management**: Create and retrieve course details.
- **Department Management**: Create and retrieve department details.
- **Attendance Tracking**: Register and retrieve student attendance.

### Prerequisites
- Python 3.11.9
- Django 5.1
- djangorestframework 3.15.2

1. **Clone the Repository**

   ```bash
   git clone https://github.com/vinaykushwaha588/attendance_api.git
   cd attendance_api
2. Create and Activate a Virtual Environment.
    python3 -m venv myenv
    myenv\Scripts\activate  or source myenv/bin/activate
3. Install Dependencies
    pip install -r requirements.txt

4. Apply Migrations
   python manage.py makemigrations
   python manage.py migrate

5. Create a Superuser
   python manage.py createsuperuser
6. Run the Development Server
   python manage.py runserver

POST_MAN Payload Collections
link - https://api.postman.com/collections/36505766-69821b04-78a8-468b-b0a3-80413c405e4c?access_key=PMAT-01J55399TKP83TT5XRF9SYWK12
** API Endpoints
● POST: http:/127.0.0.1:8000/api/user/register/ : Create a new user.
● POST: http:/127.0.0.1:8000/api/user/login: login User.
● GET: http:/127.0.0.1:8000/api/user/user_list/: UserList.
● GET: http:/127.0.0.1:8000/api/departments/: Department list.
● POST: http:/127.0.0.1:8000/api/departments/: Department Create.
● GET: http:/127.0.0.1:8000/api/course/: Course List.
● POST: http:/127.0.0.1:8000/api/course/: Course Create.
● GET: http:/127.0.0.1:8000/api/student/: Student List.
● POST: http:/127.0.0.1:8000/api/student/: Create Student.
● GET: http:/127.0.0.1:8000/api/attendance/: Attendance List.
● POST: http:/127.0.0.1:8000/api/attendance/: Attendance Create.
