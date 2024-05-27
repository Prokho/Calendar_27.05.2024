
from .viewModels import *
from .models import *
from rest_framework import serializers
from appointment.serializers import Time_slotSerializer, TimeSlotSerializer, AppointmentSerializer




class DaySerializer(serializers.Serializer):
    date = serializers.CharField()
    time_slots = serializers.IntegerField()
    busy_time_slots = serializers.IntegerField()
    possible_time_slots = serializers.IntegerField()
    def create(self, validated_data):
        return Day(**validated_data)

class RequestSchedularDaysSerializer(serializers.Serializer):
    specialist_id = serializers.IntegerField()
    def create(self, validated_data):
        return RequestSchedularDays(**validated_data)

class RequestCreateTimeSlotSerializer(serializers.Serializer):
    specialist_id = serializers.IntegerField()
    date = serializers.DateField()
    time = serializers.TimeField()
    def create(self, validated_data):
        return RequestCreateTimeSlot(**validated_data)

class ApointmentSpecialistRequestSerializer(serializers.Serializer):
    specialist_id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    phone = serializers.CharField()
    time = serializers.TimeField()
    date = serializers.DateField()
    def create(self, validated_data):
        return ApointmentSpecialistRequest(**validated_data) # смотри название класса и сам класс во viewModels.


class ListAppointmentRequestSerializer(serializers.Serializer):
    specialist_id = serializers.IntegerField()
    begin_date = serializers.DateField()
    end_date = serializers.DateField()
    def create(self, validated_data):
        return ListAppointmentRequest(**validated_data)


class ReuestDeleteTimeSlotSerializer(serializers.Serializer):
    timeslot_id = serializers.IntegerField()
    def create(self, validated_data):
        return ReuestDeleteTimeSlot(**validated_data)


class RequestDeleteAppointmentBySpecialistSerializer(serializers.Serializer):
    appointment_id = serializers.IntegerField()
    def create(self, validated_data):
        return RequestDeleteAppointmentBySpecialist(**validated_data)

class TransferAppointmentBySpecialistSerializer(serializers.Serializer):
    appointment_id = serializers.IntegerField()
    specialist_id = serializers.IntegerField()
    time = serializers.TimeField()
    date = serializers.DateField()
    def create(self, validated_data):
        return TransferAppointmentBySpecialist(**validated_data)


class ListTimeRequestSerializer(serializers.Serializer):
    specialist_id = serializers.IntegerField()
    date = serializers.DateField()
    def create(self, validated_data):
        return ListTimeRequest(**validated_data)


class TimeResponseSerializer(serializers.Serializer):
    date = serializers.DateField()
    time = serializers.TimeField()
    time_slot = TimeSlotSerializer()
    def create(self, validated_data):
        return TimeResponse(**validated_data)

class RequestAppointmentSerializer(serializers.Serializer):
    time_slot_id = serializers.IntegerField()
    def create(self, validated_data):
        return RequestAppointment(**validated_data)



