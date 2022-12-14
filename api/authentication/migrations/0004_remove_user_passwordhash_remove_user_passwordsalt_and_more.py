# Generated by Django 4.0.2 on 2022-04-10 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_refreshtoken_islatest_alter_refreshtoken_expiry_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='PasswordHash',
        ),
        migrations.RemoveField(
            model_name='user',
            name='PasswordSalt',
        ),
        migrations.AddField(
            model_name='user',
            name='Password',
            field=models.CharField(default='pbkdf2_sha256$320000$yfOSGiUmnmBGqlODy0L25p$HKR9U/074B6hQ1ThujIE8/Mm/ridT9JH4trcv3Ux7/A=', max_length=100),
            preserve_default=False,
        ),
    ]
