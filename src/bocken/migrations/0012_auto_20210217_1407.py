# Generated by Django 3.1.5 on 2021-02-17 13:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bocken', '0011_auto_20210212_1620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agreement',
            name='signed',
        ),
        migrations.AddField(
            model_name='agreement',
            name='expires',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]