# Generated by Django 3.2.6 on 2021-09-27 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_alter_userbase_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbase',
            name='gender',
            field=models.IntegerField(choices=[(None, 'not specified'), (0, 'male'), (1, 'female')], default=0, null=True),
        ),
    ]