# Generated by Django 3.1.1 on 2020-09-20 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20200920_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(default='Dashboard.owner', on_delete=django.db.models.deletion.CASCADE, to='events.dashboard'),
        ),
    ]
