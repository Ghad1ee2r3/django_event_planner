# Generated by Django 3.1.1 on 2020-09-23 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0024_auto_20200923_1236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='is_done',
        ),
    ]
