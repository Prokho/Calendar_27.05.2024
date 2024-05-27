from re import U
from django.forms import IntegerField


from .viewModels import DataRange
from .models import *
from django.contrib.auth.models import Group 
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
import datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .viewModels import RequestTimeSlotBySpecialistID, PhoneVaidateRequest, ApointmentRequest, DeleteAppointmentRequest, TransferAppointmentRequest






def time_slot_check(value):
        user = value.get("user")
        now_date = datetime.now().date()
        date_1 = value.get("date")
        time_1 = value.get("time")
        date_time_1 = datetime.combine(date_1,time_1)
        dt_prev = date_time_1 - timedelta(hours=1)
        dt_next = date_time_1 + timedelta(hours=1)
        time_prev = dt_prev.time()
        time_next = dt_next.time()
        
        errors = {}

        if user.is_active ==False: 
            errors["user"] = 'user was blocked'
        
        if not user.groups.filter(name__in=['specialist', 'manager']).exists():
            errors["groups"] = 'incorrect role'

        if date_1 < now_date:
            errors["date"] = 'incorrect date, data should be current date or future date'

        if date_1 > (now_date+relativedelta(months=+3)):
            errors["date"] = 'incorrect date,data should be not more than 3 months in future'

        if not time_1.minute %5 == 0:
            errors["time"] = 'incorrect time, time should be devided by 5'

        
        if len(Time_slot.objects.filter(time__gte=time_prev,time__lte=time_next, date=date_1, user=user))!=0:
             errors["time"] = 'incorrect time_slot'

        if len(errors)>0:
            raise serializers.ValidationError(errors)

    
def appointment_check(value):
        client = value.get("client")
        specialist = value.get("specialist")
        time_slot = value.get("time_slot")     
        dt_prev = time_slot.time - timedelta(hours=1)
        dt_next = time_slot.time + timedelta(hours=1)
        

        errors = {}

        if client.is_active ==False: 
            errors["client"] = 'client was blocked'

        if specialist.is_active ==False: 
            errors["specialist"] = 'specialist was blocked'

        if not client.groups.filter(name__in=['client']).exists():
            errors["client"] = 'incorrect role'

        if not specialist.groups.filter(name__in=['specialist']).exists():
            errors["specialist"] = 'incorrect role'

# time_slot сейчас свободен и принадлежит тому же самому психологу (передается ай ди)
        if time_slot.user.id != specialist.id:
            errors["time_slot"] = 'time_slot is held to another specialist'
        elif not time_slot.free_time:
            errors["time_slot"] = 'time_slot is busy'


# time_slot: пользователь не может создать несколько записей на одно и то же дату и время,
#  должны проверяться дата и время для записи клиента
# найти все записи клиента, среди них найти те записи, которые пересекаются с текущим тайм слотом
# из тайм слота нужно вытащить дату и время и на их основе считать пред и след час

        #if len(Appointment.objects.filter(time_slot:))!=0:
        #     errors["time_appointment_create"] = 'incorrect time_appointment' 


        if len(errors)>0:
            raise serializers.ValidationError(errors)


      

class Time_slotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time_slot
        fields = "__all__"
        validators = [time_slot_check, UniqueTogetherValidator(
                queryset=Time_slot.objects.all(),
                fields=['date', 'time', 'user']
            )]




'''API Client создаем сериалайзер для выполнения пункта 1)	получить список специалистов
на вход ничего
на выход список специалистов 
'''


class SpecialistSerializer(serializers.ModelSerializer): #///////////////
       specialist_id = serializers.ReadOnlyField(source='id') #объект согласно API
       name = serializers.ReadOnlyField(source='get_full_name') #объект согласно API
       photo = serializers.ReadOnlyField(source='user_profile_set.first.path_photo') #объект согласно API
       class Meta:
            model = User
            fields = ['specialist_id', 'photo', 'name']
            




'''API Client создаем сериалайзер для выполнения пункта 2)	получить список дат где свободные тайм слоты
На вход
дата начал диапазона
дата конца диапазона
дата начал диапазона < дата конца диапазона
На выход
Список дата
 '''

class DataRangeSerializer(serializers.Serializer):
    begin = serializers.DateField() #объект согласно API
    end = serializers.DateField() #объект согласно API
    specialist_id = serializers.IntegerField()
    online = serializers.BooleanField()

    def create(self, validated_data): #функция преобразует данные из словаря в объект
        return DataRange(**validated_data) #validated_data - находится под капотом и это словарь, котрый прошел валидацию джанго, ** - операция паревращения словаря в список аргументов и значений


class RequestTimeSlotBySpecialistIdSerializer(serializers.Serializer):
    date = serializers.DateField()
    specialist_id = serializers.IntegerField()
    online = serializers.BooleanField()

    def create(self, validated_data):
        return RequestTimeSlotBySpecialistID(**validated_data)

class TimeSlotSerializer(serializers.ModelSerializer):
    user = SpecialistSerializer()
    class Meta:
        model = Time_slot
        fields = "__all__"

class AppointmentSerializer(serializers.ModelSerializer):
    time_slot = TimeSlotSerializer()
    class Meta:
        model = Appointment
        fields = "__all__"
        validators = [appointment_check]

class PhoneVaidateRequestSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def create(self, validated_data):
        return PhoneVaidateRequest(**validated_data)

class ApointmentRequestSerializer(serializers.Serializer):
    phone = serializers.CharField()
    timeslot_id = serializers.IntegerField()
    code_validation = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()

    def create(self, validated_data):
        return ApointmentRequest(**validated_data)



class DeleteAppointmentRequestSerializer(serializers.Serializer):
    appointment_id = serializers.IntegerField()
    def create(self, validated_data):
        return DeleteAppointmentRequest(**validated_data)

#Dom
class TransferAppointmentRequestSerializer(serializers.Serializer):
    appointment_id = serializers.IntegerField()
    timeslot_id = serializers.IntegerField()
    def create(self, validated_data):
        return TransferAppointmentRequest(**validated_data)

        




