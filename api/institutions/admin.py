from django.contrib import admin
from .models import Institution, InstitutionLevel

# Register your models here.

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name')
    filter_horizontal = ('teachers' , )

admin.site.register(InstitutionLevel, admin.ModelAdmin)