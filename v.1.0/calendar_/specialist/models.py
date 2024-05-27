from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)




class ModeJobSpecialist(models.Model):
    specialist = models.ForeignKey(User, on_delete=models.RESTRICT)
    time_begin = models.TimeField()
    time_end = models.TimeField()
    duration_job_minutes = models.IntegerField()
    duration_brake_minutes = models.IntegerField()
    future_job_days = models.IntegerField(default = 90)





