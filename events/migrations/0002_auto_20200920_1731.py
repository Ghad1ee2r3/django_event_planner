# Generated by Django 3.1.1 on 2020-09-20 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(default='Dashboard.owner', on_delete=django.db.models.deletion.CASCADE, to='events.dashboard'),
        ),
    ]