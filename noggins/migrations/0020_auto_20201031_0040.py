# Generated by Django 2.2 on 2020-10-31 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noggins', '0019_auto_20201031_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nogginlike',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]