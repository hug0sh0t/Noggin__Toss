# Generated by Django 2.2 on 2020-11-01 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_profile_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.TextField(blank=True, null=True, verbose_name='auth.User'),
        ),
    ]
