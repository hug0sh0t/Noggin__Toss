# Generated by Django 2.2 on 2020-09-28 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('noggins', '0004_auto_20200927_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='noggin',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='noggins.Noggin'),
        ),
    ]