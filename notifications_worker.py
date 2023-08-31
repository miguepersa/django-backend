from api.notifications.models import PendingNotification, Notification
from datetime import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from api.notifications.consumers import NotificationConsumer
from api.notifications.serializers import NotificationSerializer

print("Running notifications worker...")

notifications = PendingNotification.objects.filter(send_date__lte=datetime.now())
print("Sending notifications...")

if len(notifications) > 0:
    for n in notifications:
        new = Notification(
            title = n.title,
            content = n.content,
            user = n.user,
            type = n.type,
            status = Notification.CREATED,
            url = n.url
        )
        new.save()

print("Notifications sent")

print("Wiping pending notifications")
notifications.delete()
print("Notifications wiped")
print("Program finished")