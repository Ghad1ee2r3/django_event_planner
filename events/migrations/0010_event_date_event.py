# Generated by Django 3.1.1 on 2020-09-20 15:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20200920_1848'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='date_event',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]