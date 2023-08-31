# Generated by Django 4.2.1 on 2023-07-12 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0051_classschedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classschedule',
            name='course_section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule', to='academic.coursesection'),
        ),
        migrations.AlterField(
            model_name='coursesection',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='academic.course'),
        ),
    ]