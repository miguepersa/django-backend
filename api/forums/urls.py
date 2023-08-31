from django.urls import path
from rest_framework.routers import DefaultRouter
from api.forums.views import *

router = DefaultRouter()
router.register(r'forums', ForumViewSet)
router.register(r'topics', ForumTopicViewSet)
router.register(r'topic_message_read_by', TopicMessageReadByViewSet)
router.register(r'topic_message', TopicMessageViewSet)