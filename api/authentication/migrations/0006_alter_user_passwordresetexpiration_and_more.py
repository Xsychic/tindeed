# Generated by Django 4.0.2 on 2022-04-26 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_user_passwordresetexpiration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='PasswordResetExpiration',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='PasswordResetToken',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
