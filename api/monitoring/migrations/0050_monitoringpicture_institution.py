# Generated by Django 4.2.1 on 2023-08-31 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0027_alter_institution_type'),
        ('monitoring', '0049_monitoringpicture'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitoringpicture',
            name='institution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='monitoring_pictures', to='institutions.institution'),
        ),
    ]