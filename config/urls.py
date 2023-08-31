"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from django.conf import settings
from django.conf.urls.static import static

from api.academic.urls import router as academic_router
from api.chats.urls import router as chat_router
from api.databank.urls import router as data_bank_router
from api.forums.urls import router as forum_router
from api.institutions.urls import router as institution_router
from api.monitoring.urls import router as monitoring_router
from api.notifications.urls import router as notifications_router
from api.users.urls import router as user_router
from api.mailer.views import index

import django_rest_passwordreset.urls

router = routers.DefaultRouter()
router.registry.extend(user_router.registry)
router.registry.extend(academic_router.registry)
router.registry.extend(institution_router.registry)
router.registry.extend(monitoring_router.registry)
router.registry.extend(notifications_router.registry)
router.registry.extend(forum_router.registry)
router.registry.extend(data_bank_router.registry)
#router.registry.extend(chat_router.registry)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

# base = "api/v1/"
base = ""

urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('', include(router.urls)),
    path(f'{base}admin/', admin.site.urls),
    path(f'{base}auth/', include('api.authentication.urls')),
    path(f'{base}users/', include('api.users.urls')),
    path(f'{base}mail_test/', index),
    #path(f'{base}institution/', include('api.institutions.urls')),
    path(f'{base}chat/', include("api.chats.urls")),
    #path(f'{base}forms/', include("api.monitoring.urls")),
    path(f'{base}password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('redoc/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='redoc'),
    path(f'{base}openapi/', get_schema_view(
        title="TecnikidsVE",
        description="TecnikidsVE REST API",
        version="1.0.0"
    ), name='openapi-schema'),

]