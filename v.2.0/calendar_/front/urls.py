from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index), # здесь ссылка на основной файл джи эс, запускающий всю логику проекта
    path('psychology/', index_specialist),# здесь ссылка на файл джи эс по логике психолога и урл этого компонента
]