# Generated by Django 2.2 on 2020-11-01 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0013_auto_20201101_0142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='username',
        ),
    ]