from rest_framework.routers import DefaultRouter
from api.notifications.views import *

router = DefaultRouter()
router.register(r'notification', NotificationViewSet)