from django.db import models
from django.utils import timezone
from api.academic.models import Lesson
from api.users.models import User
from cloudinary_storage.storage import RawMediaCloudinaryStorage

# Create your models here.


class Room(models.Model):
    name = models.CharField(blank=True, max_length=64)
    creation_date = models.DateTimeField(
        auto_now_add=True)
    status = models.CharField(max_length=64, blank=True)
    
    def __str__(self):
        if len(self.name) == 0:
            return f"Room: {self.id}"
        else:
            return f"Room: {self.name}"
        
    def last_m(self):
        messages = sorted(self.messages.all(), key = lambda x:x.id, reverse=True)
        if messages:
            return messages[0]
        
        else:
            return None
        
    def users_in_room(self):
        ur = self.user_chatroom.all()
        users = [{"id" : i.user.id, "first_name": i.user.first_name, "last_name": i.user.last_name} for i in ur]
        return users


class Message(models.Model):
    room = models.ForeignKey(
        Room, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='sent_messages', null=True, blank=True)
    status = models.CharField(max_length=64, null=True, blank=True)
    type = models.CharField(max_length=64, null=True, blank=True)
    attachment = models.FileField(upload_to='raw/', blank=True,
                            null=True, storage=RawMediaCloudinaryStorage())
    read_by = []

    def __str__(self) -> str:
        return f"Message in {self.room} by {self.created_by}"
    
    def readby(self):
        return self.read_by


class UserRoom(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='user_chatroom')
    room = models.ForeignKey(
        Room, related_name='user_chatroom', on_delete=models.CASCADE)
    date_joined = models.DateTimeField(default=timezone.now, db_index=True)
    unread_messages = models.IntegerField(default=0)

    def __str__(self):
        return f"{str(self.room)} - User: {str(self.user)}"


class ReadRoomMessage(models.Model):
    user_room = models.ForeignKey(
        UserRoom, on_delete=models.CASCADE, null=True, related_name='read_room_messages')
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name='read_room_messages')
    read_date = models.DateTimeField(null=True, blank=True)