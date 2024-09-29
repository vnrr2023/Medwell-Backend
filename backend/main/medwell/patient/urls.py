from django.urls import path
from .views import *

urlpatterns = [
    path("send_report/",send_report,name="send report"),
    path("send_status_of_task/",send_status_of_task,name="send_status_of_task"),
]
