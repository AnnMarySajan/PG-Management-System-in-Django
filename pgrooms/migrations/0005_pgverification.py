# Generated by Django 3.1.7 on 2021-06-21 14:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pgrooms', '0004_auto_20210619_1136'),
    ]

    operations = [
        migrations.CreateModel(
            name='pgverification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verifydate', models.DateTimeField(blank=True, default=None, null=True)),
                ('feedback', models.TextField(blank=True, default=None, null=True)),
                ('allotedstatus', models.BooleanField(default=True)),
                ('roomid', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pgrooms.room')),
                ('verifier', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
