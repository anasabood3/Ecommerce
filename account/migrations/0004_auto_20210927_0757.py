# Generated by Django 3.2.6 on 2021-09-27 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20210923_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbase',
            name='gender',
            field=models.CharField(choices=[(None, 'Choose your gender'), ('male', 'male'), ('female', 'female')], default=None, max_length=7),
        ),
        migrations.AlterField(
            model_name='userbase',
            name='image',
            field=models.ImageField(default='images/default.jpeg', help_text='Upload a Profile image', upload_to='images/', verbose_name='image'),
        ),
    ]
