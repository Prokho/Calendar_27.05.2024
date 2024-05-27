class Specialist:
    def __init__(self, id, name, photo):
        self.id = id
        self.name = name
        self.photo = photo

class DataRange: # объявили сериализатор в соответствии API Client для выполнения пункта 2)	получить список дат где свободные тайм слоты
    def __init__(self, begin, end, specialist_id, online):
        self.begin = begin
        self.end = end
        self.specialist_id = specialist_id
        self.online = online

class RequestTimeSlotBySpecialistID:
    def __init__(self, date, specialist_id, online):
        self.date = date
        self.specialist_id = specialist_id
        self.online = online

class PhoneVaidateRequest:
    def __init__(self, phone):
        self.phone = phone

class ApointmentRequest:
    def __init__(self, phone, timeslot_id, code_validation, name, description):
        self.phone = phone
        self.timeslot_id = timeslot_id
        self.code_validation = code_validation
        self.name = name
        self.description = description


class DeleteAppointmentRequest:
    def __init__(self, appointment_id):
        self.appointment_id = appointment_id

#dom
class TransferAppointmentRequest:
    def __init__(self, appointment_id, timeslot_id):
        self.appointment_id = appointment_id
        self.timeslot_id = timeslot_id

        


