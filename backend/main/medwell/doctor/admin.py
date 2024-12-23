from django.contrib import admin
from .models import DoctorProfile,DoctorAddress


admin.site.register(DoctorProfile)
admin.site.register(DoctorAddress)