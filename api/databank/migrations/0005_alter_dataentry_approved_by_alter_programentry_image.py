# Generated by Django 4.2.1 on 2023-06-21 13:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('databank', '0004_alter_dataentry_approved_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataentry',
            name='approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='approved_entries', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='programentry',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
