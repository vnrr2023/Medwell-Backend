from django.db import models
from authentication.models import CustomUser
import uuid
from django.contrib.postgres.fields import ArrayField

class PatientProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=200,blank=False,null=False)
    age = models.CharField(max_length=5,null=True,blank=True)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    blood_group=models.CharField(max_length=10,blank=True,null=True)
    height=models.CharField(max_length=10,blank=True,null=True)
    weight=models.CharField(max_length=10,blank=True,null=True)
    city = models.CharField(max_length=100,null=True,blank=True)  
    country = models.CharField(max_length=100,null=True,blank=True) 
    state = models.CharField(max_length=100,null=True,blank=True) 
    pin = models.CharField(max_length=10,null=True,blank=True) 
    profile_pic=models.FileField(upload_to="profilepics/",default="profile_pics/default_pp.jpg")
    profile_qr=models.FileField(upload_to="user_qrs/",null=True,blank=True)
    adhaar_card=models.FileField(upload_to="addhaar_cards/",null=True,blank=True)
    allergies = ArrayField(models.CharField(max_length=200),blank=True, default=list)
    chronic_conditions = ArrayField(models.CharField(max_length=200),blank=True, default=list)
    family_history = ArrayField(models.CharField(max_length=200),blank=True, default=list)

    
    def __str__(self) -> str:
        return self.user.email
    
class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    report_file=models.FileField(upload_to="user_reports/",null=False,blank=False)
    report_type=models.CharField(max_length=20,null=True,blank=True)
    submitted_at=models.DateField(auto_now_add=True)
    doctor_name=models.CharField(max_length=250,null=True,blank=True)
    date_of_report=models.CharField(max_length=50,null=True,blank=True)
    date_of_collection=models.CharField(max_length=50,null=True,blank=True)
    summary=models.TextField(null=True,blank=True)
    processed=models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.email


class ReportDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report=models.OneToOneField(Report,on_delete=models.CASCADE)
    hemoglobin=models.CharField(max_length=50,null=True,blank=True)
    rbc_count=models.CharField(max_length=50,null=True,blank=True)
    wbc_count=models.CharField(max_length=50,null=True,blank=True)
    platelet_count=models.CharField(max_length=50,null=True,blank=True)
    pcv=models.CharField(max_length=50,null=True,blank=True)
    bilirubin=models.CharField(max_length=50,null=True,blank=True)
    proteins=models.CharField(max_length=50,null=True,blank=True)
    calcium=models.CharField(max_length=50,null=True,blank=True)
    blood_urea=models.CharField(max_length=50,null=True,blank=True)
    sr_cholestrol=models.CharField(max_length=50,null=True,blank=True)
    report_data=models.JSONField(null=True,blank=True)


    def __str__(self) -> str:
        return self.report.user.email
    
    

class Expense(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING)
    expense_type=models.CharField(max_length=50,blank=True,null=True)
    amount=models.CharField(max_length=100,blank=True,null=True)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.email