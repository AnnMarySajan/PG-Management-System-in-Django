# Generated by Django 3.1.7 on 2021-07-26 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pgrooms', '0013_auto_20210726_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='cancelstatus',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='booking',
            name='forcecancel',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='booking',
            name='refundstatus',
            field=models.BooleanField(default=False),
        ),
    ]
