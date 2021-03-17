# Generated by Django 3.1.7 on 2021-03-16 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bocken', '0005_auto_20210316_1727'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitesettings',
            name='cost_per_mil',
        ),
        migrations.AddField(
            model_name='report',
            name='cost_per_mil',
            field=models.PositiveIntegerField(default=20, verbose_name='Cost per mil (kr)'),
        ),
    ]