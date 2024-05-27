
from datetime import datetime, timedelta, date

def validaterSlot(mode_job, time_request):
    time_request = datetime.combine(date.today(),time_request)
    t = datetime.combine(date.today(),mode_job.time_begin)
    last_time = datetime.combine(date.today(),mode_job.time_end) - timedelta(minutes=mode_job.duration_job_minutes)
    while t < last_time:
        if t == time_request:
            return True
        t += timedelta(minutes=mode_job.duration_job_minutes)
        t += timedelta(minutes=mode_job.duration_brake_minutes)
    return False


def listTime(mode_job): # возвращает список где каждый элемент списка - это время начала потенциального сеанса 
    list_time = []
    t = datetime.combine(date.today(),mode_job.time_begin)
    last_time = datetime.combine(date.today(),mode_job.time_end) - timedelta(minutes=mode_job.duration_job_minutes)
    while t < last_time:
        list_time.append(t.time())
        t += timedelta(minutes=mode_job.duration_job_minutes)
        t += timedelta(minutes=mode_job.duration_brake_minutes)
    return list_time

def listDate(mode_job): # возвращает список дат от текущей даты до текущая дата + future_job_days
    list_days = []
    current_day = datetime.now()
    future_day = current_day + timedelta(days=mode_job.future_job_days)
    while current_day <= future_day:
        list_days.append(current_day.date())
        current_day += timedelta(days=1)
    return list_days