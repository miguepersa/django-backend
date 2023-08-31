from django.urls import path
from rest_framework.routers import DefaultRouter
from api.institutions.views import *

router = DefaultRouter()
router.register(r'institution', InstitutionViewSet)
router.register(r'institution_level', InstitutionLevelViewSet)

urlpatterns = [
]
