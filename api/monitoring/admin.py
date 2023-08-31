from django.contrib import admin
from api.monitoring.models import *

# Register your models here.

admin.site.register(Announcement, admin.ModelAdmin)
admin.site.register(AnnouncementUser, admin.ModelAdmin)
admin.site.register(FormTemplate, admin.ModelAdmin)
admin.site.register(UserForm, admin.ModelAdmin)
admin.site.register(FormQuestion, admin.ModelAdmin)
admin.site.register(FormTemplateQuestion, admin.ModelAdmin)
admin.site.register(FormQuestionOption, admin.ModelAdmin)
admin.site.register(UserFormAnswer, admin.ModelAdmin)
admin.site.register(ClassJournal, admin.ModelAdmin)
admin.site.register(MonitoringForm, admin.ModelAdmin)
admin.site.register(MonitoringFormAnswer, admin.ModelAdmin)
admin.site.register(MonitoringFormQuestion, admin.ModelAdmin)
admin.site.register(Training, admin.ModelAdmin)
admin.site.register(TrainingTask, admin.ModelAdmin)