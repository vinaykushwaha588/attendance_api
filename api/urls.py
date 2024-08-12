from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user', views.UserViewSet, basename='user_registrations')


urlpatterns = [
    path('', include(router.urls)),
    path('departments/', views.DepartmentListCreateAPIView.as_view(), name='department-list-create'),
    path('course/', views.CourseListCreateAPIView.as_view(), name='course-list-create'),
    path('student/', views.StudentListCreateAPIView.as_view(), name='student-list-create'),
    path('attendance/', views.AttendanceListCreateAPIView.as_view(), name='attendance-list-create'),
]
