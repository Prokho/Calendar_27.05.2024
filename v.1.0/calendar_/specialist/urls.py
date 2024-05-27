from django.urls import include, path
from rest_framework import routers
from .views import *

#router = routers.DefaultRouter()
#router.register(r'specialist', getListSpecialist)



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [

    path('requestCreateTimeSlot/', requestCreateTimeSlot), 
# пост запрос на создание тайм слота.
# отправляем запрос в базу данных 
#"specialist_id": 2,
#   "date": "2023-08-28",
#   "time": "09:00:00"
# ответ
#{
#    "id": 15,
#    "user": {
#        "specialist_id": 2,
#        "photo": "/static/img/specialist_photo/1.jpg",
#        "name": "андрей"
#    },
#    "date": "2023-08-28",
#    "time": "09:00:00",
#    "create_date": "2023-08-26T18:29:52.167938Z",
#    "free_time": true,
#    "online": true
#}

    path('addApointment/', addApointment),
# пост на запись нового клиента
# отправляем запрос в базу данных
#"specialist_id": 3,
#    "name": "андрей_2",
#    "description": "wewewewewe",
#    "phone": "2323232323",
#    "time": "10:00:00",
#    "date": "2023-08-28"
# получаем ответ
#{
#    "id": 10,
#    "time_slot": {
#        "id": 18,
#        "user": {
#            "specialist_id": 3,
#            "photo": "/static/img/specialist_photo/2.jpg",
#            "name": "николай"
#        },
#        "date": "2023-08-28",
#        "time": "10:00:00",
#        "create_date": "2023-08-27T06:52:56.734239Z",
#        "free_time": false,
#        "online": true
#    },
#    "time_appointment_create": "2023-08-26T21:39:07.336476Z",
#    "time_appointment_delete": null,
#    "description_client": "wewewewewe",
#    "client_phone_number": "2323232323",
#    "client_name": "андрей_2",
#    "token": "GcL4zgWn8o6eTz2mzmq4vQOJUgA2XXSDQXP_unXPLrY"
#}
    path('list_apointment/', listApointment),

# пост запрос на перечень записей к конкретному психологу
# отправляем запрос в базу данных
#{
#    "specialist_id": 3,
#    "begin_date": "2023-08-28",
#    "end_date": "2023-08-28"
#}
# получаем ответ
#    {
#        "id": 10,
#        "time_slot": {
#            "id": 18,
#            "user": {
#                "specialist_id": 3,
#                "photo": "/static/img/specialist_photo/2.jpg",
#                "name": "николай"
#            },
#            "date": "2023-08-28",
#            "time": "10:00:00",
#            "create_date": "2023-08-27T06:52:56.734239Z",
#            "free_time": false,
#            "online": true
#        },
#        "time_appointment_create": "2023-08-26T21:39:07.336476Z",
#        "time_appointment_delete": null,
#        "description_client": "wewewewewe",
#        "client_phone_number": "2323232323",
#        "client_name": "андрей_2",
#        "token": "GcL4zgWn8o6eTz2mzmq4vQOJUgA2XXSDQXP_unXPLrY"
#    }
#
    path('request_delete_timeSlot/', RequestDeleteTimeSlot),
# пост запрос на возможность удалить ранее созданный таймслот
# тело запроса
#{
#    "timeslot_id": 17
#}
# ответ true, если таймслот свободен

    path('list_time/', getlistTime),
# пост запрос на возможность открыть таймслоты, не очень понятно зачем
# тело запроса
#  "specialist_id": 2,
#    "date": "2023-08-28"
# ответ
#       "date": "2023-08-28",
#        "time": "09:00:00",
#        "time_slot": {
#            "id": 15,
#            "user": {
#                "specialist_id": 2,
#                "photo": "/static/img/specialist_photo/1.jpg",
#                "name": "андрей"
#            },
#            "date": "2023-08-28",
#            "time": "09:00:00",
#            "create_date": "2023-08-26T18:29:52.167938Z",
#            "free_time": true,
#            "online": true
#        }
#    },
#    {
#        "date": "2023-08-28",
#        "time": "10:00:00",
#        "time_slot": null
#    },
#    {
#        "date": "2023-08-28",
#        "time": "11:00:00",
#        "time_slot": null
#    },
#    {
#        "date": "2023-08-28",
#        "time": "12:00:00",
#        "time_slot": null
#    },
#    {
#        "date": "2023-08-28",
#        "time": "13:00:00",
#        "time_slot": null
#    },
#    {
#        "date": "2023-08-28",
#       "time": "14:00:00",
#        "time_slot": null
#    },
#    {
#        "date": "2023-08-28",
#        "time": "15:00:00",
#        "time_slot": null
#    },
#    {
#        "date": "2023-08-28",
#        "time": "16:00:00",
#        "time_slot": null
#    },
#    {
#        "date": "2023-08-28",
#        "time": "17:00:00",
#        "time_slot": null
#

    path('Request_Schedular_Day/', getRequestSchedularDay),
# пут запрос на открытое время на 90 дней для возможного создания тайм слотов
# запрос    
# "specialist_id": 2
# ответ
#  {
#        "date": "2023-08-27",
#        "time_slots": 0,
#        "busy_time_slots": 0,
#        "possible_time_slots": 9
#    },
#    {
#        "date": "2023-08-28",
#        "time_slots": 1,
#        "busy_time_slots": 0,
#        "possible_time_slots": 8
#    },   


    path('request_delete_appointment_by_specialist/', RequestDeleteAppointment_BySpecialist),
# пут запрос на возможность удаления специалистом записи к психологу по ай ди записи
#{
#    "appointment_id": 12
#}
# ответ сервиса либо тру либо фолс


    path('transfer_apointment_by_specialist/', TransferApointment_bySpecialist),

# пут запрос на перенос записи
#{
#    "appointment_id": 17,
#    "specialist_id": 1,
#    "time": "10:00:00",
#    "date": "2023-08-28"
#}

    path('appointment_by_time_slot_id/', getAppointmentByTimeSlot_id),

# пут запрос на получение записи по ай дишнику таймслота
# запрос
#{
#    "time_slot_id": 1
#}
# ответ сервера
#{
#    "id": 1,
#    "time_slot": {
#        "id": 1,
#        "user": {
#            "specialist_id": 2,
#            "photo": "/static/img/specialist_photo/1.jpg",
#            "name": "андрей"
#        },
#        "date": "2023-08-10",
#        "time": "15:21:09",
#        "create_date": "2023-08-10T04:21:17.353766Z",
#        "free_time": false,
#        "online": true
#    },
#    "time_appointment_create": "2023-08-10T07:12:41.301998Z",
#    "time_appointment_delete": null,
#    "description_client": "empty",
#    "client_phone_number": "79067316555",
#    "client_name": "sddasd",
#    "token": "uhxtFaRwGWcLzW6amZB2JUCnmAF7B3UKm0wXpAGukfI"
#}


    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),




    
    
]

