
from django.urls import path
from .doctor_patient import refresh_patients,get_patient_reports,get_patient_health_check
from .views import add_doctor_address,get_doctor_info,get_doctor_addresses,update_doctor_profile,update_multi_media_data

urlpatterns = [
    path("refresh_patients",refresh_patients,name="refresh_patients"),
    path("get_patient_reports",get_patient_reports,name="get_patient_reports"),
    path('get_patient_health_check',get_patient_health_check,name="get_patient_health_check"),
    path('add_doctor_address',add_doctor_address,name="add_doctor_address"),
    path('get_doctor_info',get_doctor_info,name="get_doctor_info"),
    path('get_doctor_addresses',get_doctor_addresses,name="get_doctor_addresses"),
    path('save_doctor_data',update_doctor_profile,name="save_doctor_data"),
    path('save_doctor_multi_media_data',update_multi_media_data,name="save_doctor_multi_media_data"),
]