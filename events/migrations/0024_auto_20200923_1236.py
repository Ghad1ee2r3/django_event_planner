# Generated by Django 3.1.1 on 2020-09-23 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0023_auto_20200923_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='event'),
        ),
    ]
