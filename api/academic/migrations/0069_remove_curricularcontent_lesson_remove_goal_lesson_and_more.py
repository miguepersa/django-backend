# Generated by Django 4.1 on 2023-08-26 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0068_alter_learningoutcome_lesson'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curricularcontent',
            name='lesson',
        ),
        migrations.RemoveField(
            model_name='goal',
            name='lesson',
        ),
        migrations.RemoveField(
            model_name='learningoutcome',
            name='lesson',
        ),
        migrations.RemoveField(
            model_name='learningsubject',
            name='lesson',
        ),
        migrations.RemoveField(
            model_name='tpreference',
            name='lesson',
        ),
        migrations.AddField(
            model_name='lesson',
            name='curriculum_content',
            field=models.ManyToManyField(blank=True, related_name='lessons', to='academic.curricularcontent'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='curriculum_references',
            field=models.ManyToManyField(blank=True, related_name='lessons', to='academic.tpreference'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='goal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='academic.goal'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='learning_outcome',
            field=models.ManyToManyField(blank=True, related_name='lessons', to='academic.learningoutcome'),
        ),
    ]
