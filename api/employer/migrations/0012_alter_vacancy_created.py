# Generated by Django 4.0.2 on 2022-05-11 12:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0011_merge_0010_alter_vacancy_created_0010_tag_tagstyle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='Created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
