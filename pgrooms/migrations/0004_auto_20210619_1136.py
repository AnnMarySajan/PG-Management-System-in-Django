# Generated by Django 3.1.7 on 2021-06-19 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pgrooms', '0003_auto_20210617_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='gmap',
            field=models.TextField(),
        ),
    ]
