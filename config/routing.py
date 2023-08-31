from django.urls import path, re_path
from api.chats.consumers import ChatConsumer
from api.notifications.consumers import NotificationConsumer

websocket_urlpatterns = [
    # path("ws/chat/", ChatConsumer.as_asgi()),
    re_path(r"ws/chat/(?P<pk>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r"^ws/notifications/", NotificationConsumer.as_asgi())
]
