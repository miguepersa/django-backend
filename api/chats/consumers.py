# SYNCRHONOUS CONSUMER

# We recommend that you write SyncConsumers by default, and only use AsyncConsumers in cases where you know you are doing something
# that would be improved by async handling (long-running tasks that could be done in parallel) and you are only using async-native libraries.

# import json
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = "chat_%s" % self.room_name

#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name, self.channel_name
#         )
#         # Valdidate if the request user is authorized, it's recommended  that this is the last action in connect if we choose to accept
#         self.accept()

#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name, self.channel_name
#         )

#     # Receive message from WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]

#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name, {"type": "chat_message", "message": message}
#         )

#     # Receive message from room group
#     def chat_message(self, event):
#         message = event["message"]

#         # Send message to WebSocket
#         self.send(text_data=json.dumps({"message": message}))


# ASYNCHRONOUS CONSUMER
# If you really want to call a synchronous function from an AsyncConsumer, take a look at asgiref.sync.sync_to_async,
# which is the utility that Channels uses to run SyncConsumers in threadpools, and can turn any synchronous callable into an asynchronous coroutine.
#

import json

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from api.chats.models import *
from api.users.models import User
from api.chats.serializers import *
from api.users.serializers import UserSerializer
from django.dispatch import receiver
from django.db.models.signals import post_save


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["pk"]
        self.room_group_name = self.get_room_name(self.room_id)

        self.user = await self.get_user_object()
        self.room = await self.get_room_object()

        try:
            self.user_room = await self.get_user_room()

                # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

        except Exception as e:
            raise e

    async def get_user_room(self):
        return await database_sync_to_async(UserRoom.objects.get)(user=self.user, room=self.room)

    async def get_user_object(self):
        user_id = self.scope["user"].id
        return await database_sync_to_async(User.objects.get)(id=user_id)

    async def get_room_object(self):
        return await database_sync_to_async(Room.objects.get)(pk=int(self.room_id))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @staticmethod
    def get_room_name(room_id):
        return f"chat_{room_id}"

    # Receive message from WebSocket
    async def receive(self, text_data):

        data = UserSerializer(self.scope["user"]).data
        username = data["username"]
        message = text_data

        # print(f"Usuario: {username}, Mensaje: {message}")

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message",
                                   "message": message, "sender": username}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        # send message and username of sender to websocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                }
            )
        )

@receiver(post_save, sender=Message)
def send_message(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            ChatConsumer.get_room_name(instance.room.id), {
                "type" : "chat_message",
                "message" : MessageSerializer(instance).data
            }
        )