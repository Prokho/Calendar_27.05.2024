from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import secrets

def get_first_name(self):
    return f"{self.first_name} {self.last_name} "

User.add_to_class("__str__", get_first_name)

class Time_slot(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    date = models.DateField() # дата возможной записи для потенциальных клиентов
    time = models.TimeField() # время возможной записи для потенциальных клиентов
    create_date = models.DateTimeField(auto_now_add=True, blank=True) # дата и время когда психолог сделал слот доступным
    free_time = models.BooleanField(blank=True, default=True)
    online = models.BooleanField(blank=True, default=True)
    
    def __str__(self):
        return f"{self.id} {'online' if self.online else 'в кабинете'} {self.date} {self.time} {'время свободно для записи' if self.free_time else 'время занято'} {str(self.user)}"

    # для time_slot:
    # юзер не заблокирован и имеет роль специалист - для этого нужно запросить список групп и проверить что юзер принадлежит этой группе по соответствующемк ай ди.
    # ремувинг дейт - пользователь не может сам вносить данные в это поле. Поле заполняется автоматически после удаления тайм слота
    # дата должна проверяться на корректность - не младше текущей и не старше чем на 3 месяца вперед
    # минуты должны быть кратны 5-ти
    # пользователь не может создать несколько записей на одно и то же дату и время
    # новый тайм слот не пересекается с уже существующим тайм слотом (как с началом, так и концом), таймслот - берем основу на час

class Appointment(models.Model):
    time_slot = models.ForeignKey(Time_slot, on_delete=models.RESTRICT)
    time_appointment_create = models.DateTimeField(default=datetime.now())
    time_appointment_delete = models.DateTimeField(null=True, blank=True, default=None)
    description_client = models.TextField(null=True, blank=True, default=None)
    client_phone_number = models.CharField(max_length=20)
    client_name = models.CharField(max_length=50)
    token = models.CharField(max_length= 200, default=secrets.token_urlsafe())
    

    def __str__(self):
        return f"{self.time_slot.user.get_full_name()} {self.time_slot.date} {self.time_slot.time} {self.client_name} {self.client_phone_number}"



    # для appointment:
    # клиент не заблокирован и имеет правильную роль - сделано
    # специалист не заблокирован и имеет правильную роль - сделано
    # проверить что клиент принадлежит к группе клиентов, а специалист принадлежит к группе специалистов - сделано
    # time_slot сейчас свободен и принадлежит тому же самому психологу (передается ай ди)
    # time_slot: пользователь не может создать несколько записей на одно и то же дату и время, должны проверяться дата и время для записи клиента
    # time_appointment_delet - пользователь не может сам вносить данные в это поле. Поле заполняется автоматически после удаления тайм слота

class User_profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    path_photo = models.CharField(max_length=200)
    phone = models.CharField(max_length=30, default=None, null=True, blank=True)
    show = models.BooleanField(default=True, blank=True)
    time_slot_duration = models.PositiveIntegerField()
    minimal_time_start = models.TimeField()
    count_session_per_day = models.PositiveIntegerField()
    order = models.PositiveIntegerField(default=1)
    def __str__(self) -> str:
        return f'{self.id} {self.user}'

class Phone_validation(models.Model):
    phone_number = models.CharField(max_length=20)
    validation_code = models.IntegerField()







