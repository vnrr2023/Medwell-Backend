from django.urls import path
from .views import (send_status_of_task_to_mail,save_patient_info,get_patient_info,update_profile_pic ,
share_with_doctor,provide_access)
from .reports import send_report,get_reports,get_task_status
from .expenses import add_expense

urlpatterns = [
    path("send_report",send_report,name="send report"),
    path("send_status_of_task_to_mail",send_status_of_task_to_mail,name="send_status_of_task_to_mail"),
    path("get_task_status/<str:task_id>",get_task_status,name="get_task_status"),
    path("get_reports",get_reports,name="get_reports"),
    path("update_info",save_patient_info,name="update_info"),
    path("get_info",get_patient_info,name="update_info"),
    path("update_profile_pic",update_profile_pic,name="update_info"),
    path("add_expense",add_expense,name="add_expense"),
    path("share_with_doctor",share_with_doctor,name="share_with_doctor"),
    path("provide_access",provide_access,name="provide_access"),

]
