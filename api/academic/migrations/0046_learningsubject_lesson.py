# Generated by Django 4.2.1 on 2023-06-27 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0045_learningtopic_preschoolgoal_topic_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='learningsubject',
            name='lesson',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='learning_subject', to='academic.lesson'),
        ),
    ]
