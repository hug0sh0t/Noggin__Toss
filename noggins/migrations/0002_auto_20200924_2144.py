# Generated by Django 2.2 on 2020-09-25 04:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('noggins', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='noggin',
            options={'ordering': ['-id']},
        ),
    ]
