from django.contrib import admin
from api.chats.models import Room, Message, ReadRoomMessage, UserRoom


# Register your models here.
admin.site.register(Room, admin.ModelAdmin)
admin.site.register(Message, admin.ModelAdmin)
admin.site.register(ReadRoomMessage, admin.ModelAdmin)
admin.site.register(UserRoom, admin.ModelAdmin)
