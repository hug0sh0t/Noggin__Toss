# Generated by Django 2.2 on 2020-12-04 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0020_auto_20201130_0210'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='FavoredBadge',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='createBadge',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='hermesBadge',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='impactBadge',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
