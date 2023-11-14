# Generated by Django 4.2.1 on 2023-11-14 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0004_timeline_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='message_media',
            field=models.FileField(blank=True, null=True, upload_to='messages'),
        ),
        migrations.AlterField(
            model_name='timeline',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
