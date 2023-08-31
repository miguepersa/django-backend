# Generated by Django 4.2.1 on 2023-06-28 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0047_alter_program_lic'),
        ('databank', '0008_rename_name_dataentry_title_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=64)),
                ('description', models.CharField(blank=True, max_length=512)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='data_entry', to='databank.dataentry')),
                ('program', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='data_entry', to='academic.program')),
            ],
        ),
        migrations.DeleteModel(
            name='ProgramEntry',
        ),
    ]