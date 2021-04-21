# Generated by Django 3.2 on 2021-04-19 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bocken', '0006_auto_20210316_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalentry',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='journalentrygroup',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='report',
            name='cost_per_mil',
            field=models.PositiveIntegerField(default=20, help_text='Each report can have a different cost per mil. This allows the cost per mil to be changed without affecting previous reports', verbose_name='Cost per mil (kr)'),
        ),
        migrations.AlterField(
            model_name='report',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
