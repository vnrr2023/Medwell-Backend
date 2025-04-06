from django.contrib import admin
from .models import PatientProfile,Report,ReportDetail,Expense,RequestAccess

admin.site.register(PatientProfile)
admin.site.register(Report)
admin.site.register(ReportDetail)
admin.site.register(Expense)
admin.site.register(RequestAccess)
