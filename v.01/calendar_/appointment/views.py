from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from .models import Phone_validation
from .serializers import AppointmentSerializer

from .models import Appointment, Time_slot
#from rest_framework import permissions
from .migrations import *
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from .models import *
from .viewModels import * 
from rest_framework.response import Response
from random import randint
from .validation_phone import *




@api_view(["GET"]) # декоратор гет, который предварительно обрабатывает запрос гет и его проверяет (проверки под капотом)
def getListSpecialist(request): # в соответствии с апи клиента получаем список специалистов через эту функцию
    #listUser = User.objects.all() #получаем список всех специалистов, User - это имя класса импортированного на листе models.py
    # objects - требует фреймворк джанго, это атрибут    
    #list_serializable_specialist = list(map(lambda item: SpecialistSerializer(item).data, listUser))  #жесть!!!!!
    #return Response(list_serializable_specialist) 
    listUserProfile = User_profile.objects.filter(show = True).order_by('-order').all()
    listUser = list(map(lambda x: x.user, listUserProfile))
    return Response(SpecialistSerializer(listUser, many=True).data)

@api_view(["POST"]) # декоратор пост, который предварительно обрабатывает запрос пост и его проверяет (проверки под капотом)
def getListDate(request):  # в соответствии с апи клиента получаем список специалистов через эту функцию
    print(request.data['begin']) # в запросе от клиента приходят данные в виде словаря: {"begin": "2021-09-22","end": "2023-09-23"}, вид запроса описан в документации
    serializer = DataRangeSerializer(data = request.data) # создали сериализатор, чтобы десериализовать данные (из строки преврвтить их в обьект с набором полей (атрибутов) для удобства работы)
    # сам сериализатор и его поля созданы в сериалайзер пай дата рендж.
    if not serializer.is_valid(): # валидизируем данные полученные от пользователя
        return Response(serializer.errors) #сообщение об ошибке
    data_range = serializer.create(serializer.validated_data) # возвращает объект класса DataRange (данные в виде словаря, полученные в serializer, преобразуются в обьект ), validated_data - находится под капотом и это словарь, котрый прошел валидацию джанго
    # - код проверки здесь
    specialist_id = data_range.specialist_id
   
    #if Time_slot.objects.filter(user__id=data_range.specialist_id)==False:
    if not User.objects.filter(id = specialist_id).first():
        return Response({"error": "such specialist_id is not exist"})
    current_time = datetime.now()
    current_date = current_time.date()
    # с помощью validated_data отбираются нужные данные (то есть это похоже на фильтр). Изначально в предыдущих строках мы получили гораздо больше данных которые нужно отобрать.
    include_today = False
    if data_range.begin > current_date:
        list_time_slot = Time_slot.objects.filter(date__gte=data_range.begin, date__lte=data_range.end, user__id=data_range.specialist_id, free_time = True, online = data_range.online) # в скобках написать конструкцию которая принадлежит указанному диапазону, переданному пользователю, который храниться в data_range
    else:
        list_time_slot = Time_slot.objects.filter(date__gt=current_date, date__lte=data_range.end, user__id=data_range.specialist_id, free_time = True, online = data_range.online) 
        min_time = current_time + timedelta(hours=6)
        print(min_time)
        if min_time.date() <= current_date:
            time_slot_today = Time_slot.objects.filter(time__gte=min_time,date=current_date, user__id=data_range.specialist_id, free_time=True, online = data_range.online).first()
            if time_slot_today:
                include_today = True

   

    print(list_time_slot, "!!!") # получаем данные дат в указанном диапазоне в виде <QuerySet [<Time_slot: Time_slot object (1)>
    list_date = list(map(lambda item: item.date, list_time_slot))
    if include_today:
        list_date.append(current_date)
    return Response(list_date)

    

@api_view(["POST"])
def getTimeSlot(request):
    
    serializer = RequestTimeSlotBySpecialistIdSerializer(data = request.data) 
    if not serializer.is_valid(): # валидизируем данные полученные от пользователя
        return Response(serializer.errors) #сообщение об ошибке
    request_time_slot = serializer.create(serializer.validated_data)
    current_time = datetime.now()
    min_time = current_time + timedelta(hours=6)
    if current_time.date()==request_time_slot.date:
        list_time_slot = Time_slot.objects.filter(time__gte=min_time,date=request_time_slot.date, user__id=request_time_slot.specialist_id, free_time=True, online = request_time_slot.online)
    else:
        list_time_slot = Time_slot.objects.filter(date=request_time_slot.date, user__id=request_time_slot.specialist_id, free_time=True, online = request_time_slot.online)
    list_time_slot=list_time_slot.order_by("time").all()
    list_serializable_getTimeSlot = list(map(lambda item: TimeSlotSerializer(item).data, list_time_slot))
    return Response(list_serializable_getTimeSlot)

@api_view(["POST"])
def validationPhoneNumber(request):
    serializer = PhoneVaidateRequestSerializer(data = request.data)
    if not serializer.is_valid(): # валидизируем данные полученные от пользователя
        return Response(serializer.errors) 
    print(serializer.validated_data)
    validation_phone_request = serializer.create(serializer.validated_data)
    validation_code = randint(1000,9999)
    phone_validation = Phone_validation.objects.create(phone_number = validation_phone_request.phone, 
        validation_code = validation_code)
    phone_validation.save()
    code, response = validation_phone(validation_phone_request.phone, validation_code)
    return Response( code==200 and not response["errors"] and response["items"] and response["items"][0]["code"]==201)


@api_view(["POST"])
def getApointmentRequest(request):
    serializer = ApointmentRequestSerializer(data = request.data)
    if not serializer.is_valid(): # валидизируем данные полученные от пользователя
        return Response({"error": True, "payload":serializer.errors}, status=400)
    appointment_request = serializer.create(serializer.validated_data)
    phone_validation = Phone_validation.objects.filter(phone_number = appointment_request.phone, validation_code = appointment_request.code_validation).all()
    print("!!!!!!!!!!!!!!!!1", phone_validation, "96")
    if len(phone_validation) == 0 :
        return Response({"error": True,  "payload":"validation code is incorrect"}, status=404)
    time_slot = Time_slot.objects.filter(id=appointment_request.timeslot_id, free_time=True).first()
    if not time_slot:
        return Response({"error": True,  "payload":"Free timeslot not found"}, status=404)
    time_slot.free_time = False
    time_slot.save()
    appointment = Appointment.objects.create(time_slot = time_slot, 
        description_client = appointment_request.description, 
        client_phone_number = appointment_request.phone, client_name = appointment_request.name)
    appointment.save()
    send_sms(appointment_request.phone, f"вы записаны на прием к психологу на {time_slot.date} в {str(time_slot.time)[0:-3]}")
    send_sms(time_slot.user.user_profile_set.first().phone, f"к вам на прием записан клиент {appointment_request.name}, его телефон {appointment_request.phone} на {time_slot.date} в {str(time_slot.time)[0:-3]}")
    serializer_appointment = AppointmentSerializer(appointment)
    print(serializer_appointment.data)
    return Response(serializer_appointment.data)


@api_view(["POST"])
def apointmentDeleteRequest(request):
    serializer = DeleteAppointmentRequestSerializer(data = request.data)
    if not serializer.is_valid(): # валидизируем данные полученные от пользователя
        return Response(serializer.errors)
    delete_appointment_request = serializer.create(serializer.validated_data)
    id = delete_appointment_request.appointment_id
    delete_result = Appointment.objects.filter(id=id).delete()
    if delete_result[0] > 0:
        return Response(True)
    return Response(False)


@api_view(["POST"])
def apointmentTransferRequest(request):
    serializer = TransferAppointmentRequestSerializer(data = request.data)
    if not serializer.is_valid(): # валидизируем данные полученные от пользователя
        return Response(serializer.errors)
    transfer_appointment_request = serializer.create(serializer.validated_data)
    id = transfer_appointment_request.appointment_id
    time_slot = Time_slot.objects.filter(id=transfer_appointment_request.timeslot_id).first()
    transfer_appointment = Appointment.objects.filter(id=id).first()
    transfer_appointment.time_slot=time_slot # это операция присваивания, позволяет обновить поле
    transfer_appointment.save()
    serializer_appointment = AppointmentSerializer(transfer_appointment)
    return Response(serializer_appointment.data)


    #test