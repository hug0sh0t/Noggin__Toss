# Generated by Django 2.2 on 2020-11-04 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('noggins', '0021_auto_20201031_0041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noggin',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='noggins.Noggin'),
        ),
    ]
