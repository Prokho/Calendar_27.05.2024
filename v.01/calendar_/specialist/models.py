from django.db import models
from django.contrib.auth.models import User



class ModeJobSpecialist(models.Model):
    specialist = models.ForeignKey(User, on_delete=models.RESTRICT)
    time_begin = models.TimeField()
    time_end = models.TimeField()
    duration_job_minutes = models.IntegerField()
    duration_brake_minutes = models.IntegerField()
    future_job_days = models.IntegerField(default = 90)





