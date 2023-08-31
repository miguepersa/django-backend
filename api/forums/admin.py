from django.contrib import admin
from .models import Forum, ForumTopic, TopicMessage, TopicMessageReadBy

# Register your models here.
admin.site.register(Forum, admin.ModelAdmin)
admin.site.register(ForumTopic, admin.ModelAdmin)
admin.site.register(TopicMessage, admin.ModelAdmin)
admin.site.register(TopicMessageReadBy, admin.ModelAdmin)
