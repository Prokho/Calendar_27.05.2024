# Generated by Django 4.2.2 on 2023-11-19 12:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0013_alter_appointment_time_appointment_create_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='time_appointment_create',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 19, 15, 59, 1, 186236)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='token',
            field=models.CharField(default='b0FpGIlXQV_omIWpyC10AxNy1ZuYbsx9Kc6d5mpNmCI', max_length=200),
        ),
    ]
