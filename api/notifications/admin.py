from django.contrib import admin
from .models import Notification, PendingNotification


# Register your models here.
admin.site.register(Notification, admin.ModelAdmin)
admin.site.register(PendingNotification, admin.ModelAdmin)