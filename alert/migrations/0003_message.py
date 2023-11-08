# Generated by Django 4.2.1 on 2023-11-07 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0002_delete_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Messages', models.CharField(blank=True, max_length=100000)),
                ('user', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('timeline_id', models.IntegerField()),
                ('timeline_instance', models.ManyToManyField(related_name='timeline_messages', to='alert.timeline')),
            ],
        ),
    ]
