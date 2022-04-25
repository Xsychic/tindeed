# Generated by Django 4.0.2 on 2022-03-31 23:06

import authentication.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_refreshtoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='refreshtoken',
            name='IsLatest',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='refreshtoken',
            name='Expiry',
            field=models.DateTimeField(default=authentication.models.getAccessExpiry),
        ),
        migrations.AlterField(
            model_name='refreshtoken',
            name='Token',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]