# Generated by Django 3.1.5 on 2021-02-05 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bocken', '0005_auto_20210205_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agreement',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]