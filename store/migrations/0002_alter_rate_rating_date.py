# Generated by Django 3.2.4 on 2022-05-22 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='rating_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
