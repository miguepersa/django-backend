# Generated by Django 4.2.1 on 2023-07-12 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0052_alter_classschedule_course_section_and_more'),
        ('monitoring', '0029_remove_formquestion_program_formquestion_licenss'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classjournal',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='class_journal', to='academic.coursesection'),
        ),
    ]
