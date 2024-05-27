from django.contrib import admin



from .models import *
# Register your models here.


admin.site.register(Time_slot)
admin.site.register(Appointment)
admin.site.register(User_profile)
admin.site.register(Phone_validation)

