# Generated by Django 3.2.6 on 2021-09-27 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20210927_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbase',
            name='gender',
            field=models.CharField(choices=[(None, 'Choose your gender'), ('male', 'male'), ('female', 'female')], max_length=7),
        ),
    ]
