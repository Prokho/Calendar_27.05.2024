from datetime import datetime, timedelta, date

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .migrations import *
from .models import *
from .serializers import *
from .viewModels import *
from .utils import*
from appointment.models import Time_slot, Appointment
from appointment.serializers import Time_slotSerializer, TimeSlotSerializer, AppointmentSerializer
from rest_framework.permissions import IsAuthenticated


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def requestCreateTimeSlot(request):
    serializer = RequestCreateTimeSlotSerializer(data = request.data)
    if not serializer.is_valid(): # валидизируем данные полученные от пользователя
        return Response(serializer.errors) 
    
    validation_timeSlot_request = serializer.create(serializer.validated_data)# создали обьект для дальнейшей работы
    validated_specialist_id = User.objects.filter(id=validation_timeSlot_request.specialist_id).first()
    
    if not validated_specialist_id:
        return Response({"error": "such user is not exist"})
    mode_job = ModeJobSpecialist.objects.filter(specialist = validated_specialist_id).first()
  
    if validation_timeSlot_request.date < date.today():
        return Response({"error": "it is not possible to open time-slot on this data"})

    if validation_timeSlot_request.date > date.today() + timedelta(days=mode_job.future_job_days):
        return Response({"error": "it is not possible to open time-slot more than open future days"})

    if validation_timeSlot_request.time < mode_job.time_begin or validation_timeSlot_request.time > mode_job.time_end:
        return Response({"error": "Required time is out of possible time_slot"})
    
    if not validaterSlot(mode_job, validation_timeSlot_request.time):
            return Response({"error": "Required time is out of possible open time for service"})

    new_time_slot = Time_slot.objects.create(user=validated_specialist_id, time=validation_timeSlot_request.time, date=validation_timeSlot_request.date, create_date=datetime.now(), free_time = True)
    
    new_time_slot.save()
    serializer_time_slot = TimeSlotSerializer(new_time_slot)
    return Response(serializer_time_slot.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addApointment(request):
    serializer = ApointmentSpecialistRequestSerializer(data = request.data)
    if not serializer.is_valid(): # валидизируем данные полученные от пользователя
        return Response(serializer.errors) 

    appointment_request = serializer.create(serializer.validated_data)# создали обьект для дальнейшей работы
    specialist = User.objects.filter(id=appointment_request.specialist_id).first() # 

    if not specialist:
        return Response({"error": "such user is not exist"})

    open_time_slot = Time_slot.objects.filter(time=appointment_request.time, date = appointment_request.date, user = specialist).first()

    if open_time_slot and not open_time_slot.free_time:
        return Response({"error": "time_slot is busy"})

    if not open_time_slot:
        mode_job = ModeJobSpecialist.objects.filter(specialist = specialist).first()
        if appointment_request.date < date.today():
            return Response({"error": "it is not possible to open time-slot on this data"})
        if appointment_request.date > date.today() + timedelta(days=mode_job.future_job_days):
            return Response({"error": "it is not possible to open time-slot more than open future days"})
        if appointment_request.time < mode_job.time_begin or appointment_request.time > mode_job.time_end:
            return Response({"error": "Required time is out of possible time_slot"})
        if not validaterSlot(mode_job, appointment_request.time):
            return Response({"error": "Required time is out of possible open time for service"})
        open_time_slot = Time_slot.objects.create(user=specialist, time=appointment_request.time, date=appointment_request.date, create_date=datetime.now())  
        open_time_slot.save()

        appointment_by_specialist = Appointment.objects.create(time_slot = open_time_slot, 
        description_client = appointment_request.description, 
        client_phone_number = appointment_request.phone, client_name = appointment_request.name)
        appointment_by_specialist.save()
        open_time_slot.free_time = False
        open_time_slot.save()

        serializer_appointment = AppointmentSerializer(appointment_by_specialist)
        return Response(serializer_appointment.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def listApointment(request):
    serializer = ListAppointmentRequestSerializer(data = request.data)
    if not serializer.is_valid(): # валидизируем данные полученные от пользователя
        return Response(serializer.errors) 
    list_appointment_request = serializer.create(serializer.validated_data)# создали обьект для дальнейшей работы
    specialist = User.objects.filter(id=list_appointment_request.specialist_id).first()
    if not specialist:
        return Response({"error": "such user is not exist"})
    if list_appointment_request.begin_date > list_appointment_request.end_date:
        return Response({"error": "required data parametrs are incorrect"})
    list_appointment = Appointment.objects.filter(time_slot__user = specialist, time_slot__date__gte = list_appointment_request.begin_date, time_slot__date__lte = list_appointment_request.end_date)
    serializer_appointment = AppointmentSerializer(list_appointment, many = True)
    return Response(serializer_appointment.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def RequestDeleteTimeSlot(request):
    serializer = ReuestDeleteTimeSlotSerializer(data = request.data)
    if not serializer.is_valid(): # валидизируем данные полученные от пользователя
        return Response(serializer.errors) 
    delete_timeslot_request = serializer.create(serializer.validated_data)
    id = delete_timeslot_request.timeslot_id
    delete_result = Time_slot.objects.filter(id=id).delete()
    if delete_result[0] > 0:
        return Response(True)
    return Response(False)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def RequestDeleteAppointment_BySpecialist(request):
    serializer = RequestDeleteAppointmentBySpecialistSerializer(data = request.data)
    if not serializer.is_valid(): # валидизируем данные полученные от пользователя
        return Response(serializer.errors) 
    delete_appointment_request = serializer.create(serializer.validated_data)
    id = delete_appointment_request.appointment_id
    delete_result = Appointment.objects.filter(id=id).delete()
    if delete_result[0] > 0:
        return Response(True)
    return Response(False)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def TransferApointment_bySpecialist(request):
    serializer = TransferAppointmentBySpecialistSerializer(data = request.data)
    if not serializer.is_valid(): # валидизируем данные полученные от пользователя
        return Response(serializer.errors)
    transfer_appointment_request = serializer.create(serializer.validated_data)
    id = transfer_appointment_request.appointment_id

    transfer_appointment = Appointment.objects.filter(id=id).first()
    if not transfer_appointment:
         return Response({"error": "such appointment is not exist"})

    specialist = User.objects.filter(id=transfer_appointment_request.specialist_id).first() # 

    if not specialist:
        return Response({"error": "such user is not exist"})

    open_time_slot = Time_slot.objects.filter(time=transfer_appointment_request.time, date = transfer_appointment_request.date, user = specialist).first()

    if open_time_slot and not open_time_slot.free_time:
        return Response({"error": "time_slot is busy"})

    if not open_time_slot:
        mode_job = ModeJobSpecialist.objects.filter(specialist = specialist).first()
        if transfer_appointment_request.date < date.today():
            return Response({"error": "it is not possible to open time-slot on this data"})
        if transfer_appointment_request.date > date.today() + timedelta(days=mode_job.future_job_days):
            return Response({"error": "it is not possible to open time-slot more than open future days"})
        if transfer_appointment_request.time < mode_job.time_begin or transfer_appointment_request.time > mode_job.time_end:
            return Response({"error": "Required time is out of possible time_slot"})
        if not validaterSlot(mode_job, transfer_appointment_request.time):
            return Response({"error": "Required time is out of possible open time for service"})
        open_time_slot = Time_slot.objects.create(user=specialist, time=transfer_appointment_request.time, date=transfer_appointment_request.date, create_date=datetime.now())  
        open_time_slot.save()

    
    preview_time_slot = transfer_appointment.time_slot
    preview_time_slot.free_time = True
    preview_time_slot.save()
    transfer_appointment.time_slot=open_time_slot # это операция присваивания, позволяет обновить поле
    transfer_appointment.save()
    open_time_slot.free_time = False
    open_time_slot.save()
    serializer_appointment = AppointmentSerializer(transfer_appointment)
    return Response(serializer_appointment.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def getlistTime(request):
    serializer = ListTimeRequestSerializer(data = request.data)
    if not serializer.is_valid(): # валидизируем данные полученные от пользователя
        return Response(serializer.errors)
    list_time_request = serializer.create(serializer.validated_data)
    
    specialist = User.objects.filter(id=list_time_request.specialist_id).first() # 
    if not specialist:
        return Response({"error": "such user is not exist"})

    mode_job = ModeJobSpecialist.objects.filter(specialist = specialist).first()

    list_time = listTime(mode_job)
    list_time_response = []
    for t in list_time:
        time_slot = Time_slot.objects.filter(time = t, date = list_time_request.date, user = specialist).first()
        list_time_response.append(TimeResponse(list_time_request.date, t, time_slot))

    serializer_timeresponse = TimeResponseSerializer(list_time_response, many = True)
    return Response(serializer_timeresponse.data)
    # создать сериалайзер для тайим респонс, сериализовать лист тайм респонс и сделать ретерн респонс.


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def getAppointmentByTimeSlot_id(request):
    serializer = RequestAppointmentSerializer(data = request.data)
    if not serializer.is_valid(): # валидизируем данные полученные от пользователя
        return Response(serializer.errors)
    request_appointment = serializer.create(serializer.validated_data)
    time_slot = Time_slot.objects.filter(id = request_appointment.time_slot_id).first()
    if not time_slot:
        return Response({"error": "such time_slot is not exist"})
    if time_slot.free_time:
        return Response({"error": "such time_slot is not busy"})
    appointment = Appointment.objects.filter(time_slot=time_slot).first()
    if not appointment:
        return Response({"error": "such appointment for this time_slot is not exist"})
    serializer_appointment = AppointmentSerializer(appointment)
    return Response(serializer_appointment.data)

    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def getRequestSchedularDay(request):
    serializer = RequestSchedularDaysSerializer(data = request.data)
    if not serializer.is_valid(): # валидизируем данные полученные от пользователя
        return Response(serializer.errors)
    request_schedular_days = serializer.create(serializer.validated_data)
    specialist_id = request_schedular_days.specialist_id
    specialist = User.objects.filter(id=specialist_id).first()
    if not specialist:
        return Response({"error": "such user is not exist"})
    mode_job = ModeJobSpecialist.objects.filter(specialist = specialist).first()
        
    list_time = listTime(mode_job)    
    list_date = listDate(mode_job) 
    list_days = []
    for date in list_date:
        count_busy_time_slot = Time_slot.objects.filter(free_time = False,  date = date , user = specialist_id).count()
        count_total_time_slot = Time_slot.objects.filter(date = date , user = specialist_id).count()
        count_possible_time_slot = len(list_time) - count_total_time_slot
        list_days.append(Day(date, count_total_time_slot, count_busy_time_slot, count_possible_time_slot))
    serializer_days = DaySerializer(list_days, many=True)
    return Response(serializer_days.data)



