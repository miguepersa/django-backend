from django.contrib import admin
from api.databank.models import DataEntry, RelatedEntry
from api.databank.forms import DataEntryForm, RelatedEntryForm

# Register your models here.
@admin.register(RelatedEntry)
class RelatedEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'entry', 'title', 'program')
    form = RelatedEntryForm

@admin.register(DataEntry)
class DataEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'updated_by', 'updated_at', 'approved_by', 'approved_date', 'status')
    form = DataEntryForm