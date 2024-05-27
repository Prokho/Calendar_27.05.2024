

class Day:
    def __init__(self, date, time_slots, busy_time_slots, possible_time_slots):
        self.date = date
        self.time_slots = time_slots
        self.busy_time_slots = busy_time_slots
        self.possible_time_slots = possible_time_slots

class RequestSchedularDays:
    def __init__(self, specialist_id):
        self.specialist_id = specialist_id


class RequestCreateTimeSlot:
    def __init__(self, specialist_id, date, time):
        self.specialist_id = specialist_id
        self.date = date
        self.time = time

class ApointmentSpecialistRequest:
    def __init__(self, specialist_id, name, description, phone, time, date):
        self.specialist_id = specialist_id
        self.name = name
        self.description = description
        self.phone = phone
        self.date = date
        self.time = time


class ListAppointmentRequest:
    def __init__(self, specialist_id, begin_date, end_date):
        self.specialist_id = specialist_id
        self.begin_date = begin_date
        self.end_date = end_date

class ReuestDeleteTimeSlot:
    def __init__(self, timeslot_id):
        self.timeslot_id = timeslot_id


class RequestDeleteAppointmentBySpecialist:
    def __init__(self, appointment_id):
        self.appointment_id = appointment_id
        
class TransferAppointmentBySpecialist:
    def __init__(self, appointment_id, specialist_id, date, time):
        self.appointment_id = appointment_id
        self.specialist_id = specialist_id
        self.date = date
        self.time = time

class ListTimeRequest:
    def __init__(self, specialist_id, date):
        self.specialist_id = specialist_id
        self.date = date

class TimeResponse:
    def __init__(self, date, time, time_slot):
        self.date = date
        self.time = time
        self.time_slot = time_slot

class RequestAppointment:
    def __init__(self, time_slot_id):
        self.time_slot_id = time_slot_id
        