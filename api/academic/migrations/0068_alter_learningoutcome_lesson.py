# Generated by Django 4.1 on 2023-08-26 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0067_remove_learningoutcome_lesson_learningoutcome_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learningoutcome',
            name='lesson',
            field=models.ManyToManyField(blank=True, related_name='learning_outcomes', to='academic.lesson'),
        ),
    ]