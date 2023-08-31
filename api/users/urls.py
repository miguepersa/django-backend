from django.urls import path, include
from api.users.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'accounts', UserViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'upload', UploadViewSet, basename="upload")

urlpatterns = [
    path("", include(router.urls)),
    path('profile/', ProfileView.as_view()),
    path('profile/<int:pk>', ProfileView.as_view()),
]
