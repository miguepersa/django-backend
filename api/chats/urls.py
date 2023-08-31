from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.chats.views import RoomViewset, MessageViewSet, UserRoomViewset

router = DefaultRouter()
router.register(r'room', RoomViewset)
router.register(r'message', MessageViewSet)
router.register(r'user_rooms', UserRoomViewset)

urlpatterns = [
    path("", include(router.urls)),
    # path("<str:room_name>/", room, name="room"),
]
