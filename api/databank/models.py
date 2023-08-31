from django.db import models
from api.users.models import User
from api.academic.models import Program

# Create your models here.
class DataEntry(models.Model):

    APPROVED = 'APPROVED'
    NOT_APPROVED = 'NOT_APPROVED'
    PENDING = 'PENDING'

    STATUS_CHOICES = [
        (APPROVED, 'Approved'),
        (NOT_APPROVED, 'Not Approved'),
        (PENDING, 'Pending')
    ]

    title = models.CharField(max_length=128, blank=False, unique=True, editable=True)

    content = models.CharField(max_length=512, blank=False, editable=True)

    url = models.URLField(blank=True)

    updated_by = models.ForeignKey(User, related_name='updated_entries', blank=True, on_delete=models.DO_NOTHING, null=True)

    updated_at = models.DateTimeField(auto_now_add=True)

    approved_by = models.ForeignKey(User, related_name='approved_entries', blank=True, null=True, on_delete=models.DO_NOTHING)

    approved_date = models.DateTimeField(blank=True, null=True)

    status = models.CharField(max_length=32,choices=STATUS_CHOICES, blank=True)

    # data_entry = id of ProgramEntry object

    def __str__(self):
        return self.title


class RelatedEntry(models.Model):
    title = models.CharField(max_length=64, blank=True)

    description = models.CharField(max_length=512, blank=True)

    program = models.ForeignKey(Program, related_name='data_entry', on_delete=models.DO_NOTHING, null=True, blank=True)

    entry = models.ForeignKey(DataEntry, related_name='data_entry', on_delete=models.DO_NOTHING)

    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.entry.title + " | " +  self.title
