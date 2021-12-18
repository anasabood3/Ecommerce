# Generated by Django 3.2.6 on 2021-09-27 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_alter_userbase_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbase',
            name='gender',
            field=models.CharField(blank=True, choices=[('None', 'not specified'), ('male', 'male'), ('female', 'female')], default=0, max_length=7),
        ),
    ]