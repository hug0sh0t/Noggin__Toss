# Generated by Django 2.2 on 2020-11-02 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0016_auto_20201101_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='noggintag',
            field=models.CharField(blank=True, default='defaultnoggintag', max_length=90, null=True),
        ),
    ]
