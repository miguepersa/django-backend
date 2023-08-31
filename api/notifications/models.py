from django.db import models
from api.users.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.dispatch import receiver
from django.db.models.signals import post_save

from api.forums.models import TopicMessage
from api.monitoring.models import AnnouncementUser, UserForm, Training
from api.chats.models import Message
# Create your models here.

import datetime

class Notification(models.Model):

    CREATED = 1
    DELIVERED = 2
    READ = 3

    NOTIFICATION_STATUS = [
        (CREATED, "Created"),
        (DELIVERED, "Delivered"),
        (READ, "Read")
    ]

    title = models.CharField(max_length=45)

    content = models.CharField(max_length=100)

    creation_date = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, )

    type = models.CharField(max_length=32)

    status = models.IntegerField(choices=NOTIFICATION_STATUS, default=CREATED)

    url = models.URLField(blank=True)

    def __str__(self):
        return f"Notification: {self.title} to {str(self.user)}"


class PendingNotification(models.Model):

    title = models.CharField(max_length=45)

    content = models.CharField(max_length=100)

    creation_date = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, )

    type = models.CharField(max_length=32)

    url = models.URLField(blank=True)

    send_date = models.DateTimeField()

    def __str__(self):
        return f"Pending Notification: {self.title} to {str(self.user)}"


@receiver(post_save, sender=AnnouncementUser)
def announcement_handler(sender, instance, created, **kwargs): 
    if instance.announcement.start_date <= datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=-4))):
        new_notification = Notification(
            title = "Nuevo anuncio",
            content = instance.announcement.title,
            user = instance.user,
            type = "Announcement",
            status = Notification.CREATED,
            url = f"/announcement/{instance.announcement.id}/"
        )
        new_notification.save()

    else:
        pending_notification = PendingNotification(
            title = "New Announcement",
            content = instance.announcement.title,
            user = instance.user,
            type = "Announcement",
            url = f"/announcement/{instance.announcement.id}/",
            send_date = instance.announcement.start_date
        )
        pending_notification.save()

@receiver(post_save, sender=UserForm)
def survey_handler(sender, instance, created, **kwargs):
    if instance.form_template.start_date <= datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=-4))):
        new_notification = Notification(
            title = "New Form",
            content = instance.form_template.name,
            user = instance.user,
            type = "Form",
            status = Notification.CREATED,
            url = f"/user_form/{instance.id}/"
        )
        new_notification.save()

    else:
        pending_notification = PendingNotification(
            title = "New Form",
            content = instance.form_template.name,
            user = instance.user,
            type = "Form",
            url = f"/user_form/{instance.id}/",
            send_date = instance.form_template.start_date
        )
        pending_notification.save()

@receiver(post_save, sender=Training)
def training_handler(sender, instance, created, **kwargs):
    if instance.start_date <= datetime.date(datetime.today()):
        for t in instance.teachers.all():
            new_notification = Notification(
                title = "New Training",
                content = instance.title,
                user = t,
                type = "Training",
                status = Notification.CREATED,
                url = f"/training/{instance.id}/"
            )
            new_notification.save()

    else:
        for t in instance.teachers.all():
            pending_notification = PendingNotification(
                title = "New Training",
                content = instance.title,
                user = t,
                type = "Training",
                url = f"/training/{instance.id}/",
                send_date = instance.start_date
            )
            pending_notification.save()

@receiver(post_save, sender=Message)
def chat_message_handler(sender, instance, created, **kwargs): 
    for u in instance.room.user_chatroom.all():
        new_notification = Notification(
            title = "New Message",
            content = f"New message in {u.room.name}",
            user = u.user,
            type = "Chat",
            status = Notification.CREATED,
            url = f"/room/{instance.room.id}/"
        )
        new_notification.save()

@receiver(post_save, sender=TopicMessage)
def topic_message_handler(sender, instance, created, **kwargs): 
    for u in instance.topic.forum.members.all():
        new_notification = Notification(
            title = "New Topic Message",
            content = f"New message in topic {instance.topic.title}",
            user = u,
            type = "Forum Topic message",
            status = Notification.CREATED,
            url = f"/topics/{instance.topic.id}/"
        )
        new_notification.save()