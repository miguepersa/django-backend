# Generated by Django 4.2.1 on 2023-05-16 19:31

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institutions', '0008_institution_level'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='institution_level',
            new_name='InstitutionLevel',
        ),
    ]