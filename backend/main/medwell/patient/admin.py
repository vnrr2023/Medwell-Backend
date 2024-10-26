from django.contrib import admin
from .models import PatientProfile,Report,ReportDetail,Expense
# Register your models here.

admin.site.register(PatientProfile)
admin.site.register(Report)
admin.site.register(ReportDetail)
admin.site.register(Expense)
