# Generated by Django 4.0.2 on 2022-03-08 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='PasswordResetExpiration',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='PasswordResetToken',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
