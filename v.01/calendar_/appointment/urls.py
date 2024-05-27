from django.urls import include, path
from rest_framework import routers
from .views import *

#router = routers.DefaultRouter()
#router.register(r'specialist', getListSpecialist)



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
#    path('', include(router.urls)),
    path('specialist/', getListSpecialist), #создали урлы согласно API
    path('get_freedate_list/', getListDate), #оздали урлы согласно API
    path('get_time_slot/', getTimeSlot), #оздали урлы согласно API
    path('validation_phone_number/', validationPhoneNumber), #оздали урлы согласно API
    path('appointment/', getApointmentRequest), #оздали урлы согласно API
    path('delete_appointment/', apointmentDeleteRequest), #оздали урлы согласно API
    path('transfer_appointment/', apointmentTransferRequest), #оздали урлы согласно API
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')), 
    
]

