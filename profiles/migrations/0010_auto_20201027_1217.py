# Generated by Django 2.2 on 2020-10-27 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_auto_20201026_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='default-avatar.png', null=True, upload_to='avatars/%Y/%m/%d/'),
        ),
    ]
