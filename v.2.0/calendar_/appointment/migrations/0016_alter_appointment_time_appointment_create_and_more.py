# Generated by Django 4.2.2 on 2023-11-19 13:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0015_alter_appointment_time_appointment_create_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='time_appointment_create',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 19, 16, 2, 35, 5315)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='token',
            field=models.CharField(default='9uY-UxFE9NucG2m0gsOa8vVBGP5LH4I0XMXNN99n0SA', max_length=200),
        ),
    ]
