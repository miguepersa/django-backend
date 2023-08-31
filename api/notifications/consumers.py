import asyncio
import ast
import json
from api.users.models import User
from api.notifications.models import Notification
from api.notifications.serializers import NotificationSerializer
from channels.consumer import AsyncConsumer
from channels.db import DatabaseSyncToAsync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import send_mail
from config.settings.base import EMAIL_HOST_USER
from django.dispatch import receiver
from django.db.models.signals import post_save

class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = await self.get_user_object()
        await self.channel_layer.group_add(
            self.get_group_name(self.user.id),
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.get_group_name(self.user.id),
            self.channel_name
        )

    async def get_user_object(self):
        user_id = self.scope["user"].id
        return await database_sync_to_async(User.objects.get)(id=user_id)

    @staticmethod
    def get_group_name(user_id):
        return f'user_{user_id}'    
    
    async def receive(self, text_data):
        users = string_to_list(text_data)            
        for u in users:
            group = self.get_group_name(u)
            await self.channel_layer.group_send(group, {
                "type" : "new_notification",
                "message": "New Notification"
            })

    async def new_notification(self, event):
        notification = event['notification']
        await self.send(text_data=json.dumps({'notification' : notification}))



@receiver(post_save, sender=Notification)    
def notify (sender, instance, created, **kwargs): 
    if created: 
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(

            NotificationConsumer.get_group_name(instance.user.id), {
                "type" : "new_notification",
                "notification": NotificationSerializer(instance).data
            }
        )

        if instance.type == "Training" or instance.type == "Announcement" or instance.type == "Form":
            bodies = {
                "Training" : "asdas",
                "Announcement" : "asdasd",
                "Form" : "asdsasd"
            }

            context = {
                'user': f"{instance.user.first_name} {instance.user.last_name}",
                'email': instance.user.email,
                'content' : bodies['instance.type'],
                'url' : ""
            }

            template = 'notifications/notification_mail.html'
            email_plaintext_message = render_to_string(template, context)


            send_mail(
                # title:
                instance.title,
                # message:
                '',
                # from:
                EMAIL_HOST_USER,
                # to:
                [instance.user.email],
                False,
                html_message=email_plaintext_message

            )

        

def string_to_list(string_repr):
    try:
        result_list = ast.literal_eval(string_repr)
        if not isinstance(result_list, list):
            raise ValueError("The input string does not represent a list.")
        return result_list
    except (SyntaxError, ValueError) as e:
        # If the string can't be parsed as a list, an exception will be raised.
        # You can handle the error as you see fit.
        print(f"Error: {e}")
        return []