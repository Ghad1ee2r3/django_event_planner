# Generated by Django 3.1.1 on 2020-09-21 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_bookingevent_nameevent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookingevent',
            old_name='ticket',
            new_name='ticketnumber',
        ),
    ]
