# Generated by Django 4.2.1 on 2023-05-23 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0025_remove_course_scholar_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='academic_year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='year_courses', to='academic.scholaryear'),
        ),
    ]
