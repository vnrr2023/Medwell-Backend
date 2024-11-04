from django.urls import path
from .views import (send_status_of_task_to_mail,save_patient_info,health_check,get_patient_info,update_profile_pic ,
share_with_doctor,patient_dashboard)
from .reports import send_report,get_report_task_status,get_reports
from .expenses import add_expense,show_expenses,expenses_dashboard,delete_expense

urlpatterns = [
    path("send_report/",send_report,name="send report"),
    path("send_status_of_task_to_mail/",send_status_of_task_to_mail,name="send_status_of_task_to_mail"),
    path("get_report_task_status/",get_report_task_status,name="get_report_task_status"),
    path("get_reports/",get_reports,name="get_reports"),
    path("health_check/",health_check,name="health_check"),
    path("update_info/",save_patient_info,name="update_info"),
    path("get_info/",get_patient_info,name="update_info"),
    path("update_profile_pic/",update_profile_pic,name="update_info"),
    path("add_expense/",add_expense,name="add_expense"),
    path("show_expenses/",show_expenses,name="show_expenses"),
    path("expenses_dashboard/",expenses_dashboard,name="expenses_dashboard"),
    path("delete_expense/",delete_expense,name="delete_expense"),
    path("share_with_doctor/",share_with_doctor,name="share_with_doctor"),
    path("dashboard/",patient_dashboard,name="dashboard"),
]
