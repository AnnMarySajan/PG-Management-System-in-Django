# Generated by Django 3.1.7 on 2021-07-23 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pgrooms', '0008_cancelledbooking'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='payment',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
