from django.contrib import admin
from .models import DoctorProfile,DoctorAddress,DoctorServices,AppointmentSlot,Appointment,AppointmentPayment,ServiceMarketting


admin.site.register(DoctorProfile)
admin.site.register(DoctorAddress)
admin.site.register(DoctorServices)
admin.site.register(AppointmentSlot)
admin.site.register(Appointment)
admin.site.register(AppointmentPayment)
admin.site.register(ServiceMarketting)