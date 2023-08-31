# Generated by Django 4.1 on 2023-05-19 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0020_alter_lesson_achievement_indicators_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='reference_number',
            field=models.FloatField(default=1.0),
        ),
        migrations.AlterField(
            model_name='lessonprogram',
            name='lesson_number',
            field=models.IntegerField(blank=True, default=1),
        ),
        migrations.AlterField(
            model_name='lessonprogram',
            name='term',
            field=models.IntegerField(choices=[(1, 'Primer Lapso'), (2, 'Segundo Lapso'), (3, 'Tercer Lapso')], default=-1),
        ),
    ]
