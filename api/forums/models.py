from django.db import models
from api.users.models import User
from api.academic.models import Course, Lesson
from cloudinary_storage.storage import RawMediaCloudinaryStorage


from datetime import datetime
# Create your models here.


class Forum(models.Model):
    description = models.CharField(max_length=512, blank=True)

    course = models.OneToOneField(
        Course, related_name='forum', on_delete=models.SET_NULL, null=True)

    members = models.ManyToManyField(User, related_name='forums')

    # forum_topics = topics in the forum

    def __str__(self):
        return f"Foro: {str(self.course)}"


class ForumTopic(models.Model):

    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    HIDDEN = 'HIDDEN'

    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
        (HIDDEN, 'Hidden')
    ]

    title = models.CharField(max_length=256)

    description = models.CharField(max_length=512, blank=True)

    status = models.CharField(
        max_length=32, choices=STATUS_CHOICES, default=OPEN)

    start_date = models.DateField(auto_now_add=True)

    end_date = models.DateField(blank=True, null=True)

    forum = models.ForeignKey(
        Forum, related_name='forum_topics', on_delete=models.SET_NULL, null=True)

    lesson = models.ForeignKey(
        Lesson, related_name='forum_topics', on_delete=models.SET_NULL, null=True, blank=True)
    
    last_interaction = models.DateTimeField(default=datetime.min)

    # topic_messages = forum messages

    def __str__(self):
        return str(self.forum) + ' | ' + self.title

    def getNumberOfMessages(self):
        return len(self.topic_messages.all())

class TopicMessage(models.Model):
    content = models.CharField(max_length=45)

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='topic_messages')

    date = models.DateTimeField(auto_now_add=True)

    previous_version = models.OneToOneField(
        'self', on_delete=models.SET_NULL, null=True, related_name='new_version', blank=True)

    # new_version = new version of the message

    archived = models.BooleanField(default=False)

    responds_to = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, related_name='responses', blank=True)

    # responses ^

    type = models.CharField(max_length=255, blank=True)

    topic = models.ForeignKey(
        ForumTopic, related_name='topic_messages', on_delete=models.SET_NULL, null=True)

    text = models.CharField(max_length=64, blank=True)

    attachment = models.FileField(upload_to='raw/', blank=True,null=True, storage=RawMediaCloudinaryStorage())

    # read_by

    def __str__(self):
        return 'Message #:' + str(self.id)


class TopicMessageReadBy(models.Model):
    message = models.ForeignKey(
        TopicMessage, related_name='read_by', on_delete=models.SET_NULL, null=True)

    user = models.ForeignKey(
        User, related_name='read_forum_messages', on_delete=models.SET_NULL, null=True)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.message) + ' read by: ' + self.user.username
