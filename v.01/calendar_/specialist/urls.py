from django.urls import include, path
from rest_framework import routers
from .views import *

#router = routers.DefaultRouter()
#router.register(r'specialist', getListSpecialist)



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
#    path('', include(router.urls)),
    path('requestCreateTimeSlot/', requestCreateTimeSlot), #создали урлы согласно API
    path('addApointment/', addApointment),
    path('list_apointment/', listApointment),
    path('request_delete_timeSlot/', RequestDeleteTimeSlot),
    path('list_time/', getlistTime),
    path('Request_Schedular_Day/', getRequestSchedularDay),
    path('request_delete_appointment_by_specialist/', RequestDeleteAppointment_BySpecialist),
    path('transfer_apointment_by_specialist/', TransferApointment_bySpecialist),
    path('appointment_by_time_slot_id/', getAppointmentByTimeSlot_id),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    
]

