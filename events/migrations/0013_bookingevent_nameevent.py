# Generated by Django 3.1.1 on 2020-09-21 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_bookingevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingevent',
            name='nameEvent',
            field=models.CharField(default=1, max_length=120),
            preserve_default=False,
        ),
    ]