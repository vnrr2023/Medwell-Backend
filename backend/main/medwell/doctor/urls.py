
from django.urls import path
from .views import refresh_patients,get_patient_reports,get_patient_health_check
urlpatterns = [
    path("refresh_patients/",refresh_patients,name="refresh_patients"),
    path("get_patient_reports/",get_patient_reports,name="get_patient_reports"),
    path('get_patient_health_check/',get_patient_health_check,name="get_patient_health_check")
]