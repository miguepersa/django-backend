# Generated by Django 4.2.1 on 2023-08-04 15:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institutions', '0024_alter_institutionlevel_student_sections_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='monitor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='institutions', to=settings.AUTH_USER_MODEL),
        ),
    ]
