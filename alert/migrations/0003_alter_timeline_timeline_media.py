# Generated by Django 4.2.1 on 2023-10-22 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0002_remove_reaction_timeline_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeline',
            name='timeline_media',
            field=models.FileField(blank=True, null=True, upload_to='timeline'),
        ),
    ]