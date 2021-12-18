# Generated by Django 3.2.6 on 2021-09-27 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_alter_userbase_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbase',
            name='gender',
            field=models.IntegerField(choices=[(None, ''), (0, 'male'), (1, 'female'), (2, 'not specified')], default=2, null=True),
        ),
    ]
