# Generated by Django 3.1.5 on 2021-02-03 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bocken', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalentry',
            name='group',
            field=models.CharField(choices=[], max_length=120),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='name',
            field=models.CharField(max_length=120),
        ),
    ]