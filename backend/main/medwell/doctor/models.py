from django.db import models
from authentication.models import CustomUser
from patient.models import PatientProfile
from uuid import uuid4
from datetime import datetime


class DoctorProfile(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    name=models.CharField(max_length=400,blank=False,null=False)
    phone_number=models.CharField(max_length=12,blank=False,null=False)
    dob=models.DateField(blank=True,null=True)
    speciality=models.CharField(max_length=250,null=True,blank=True)
    verified=models.BooleanField(default=False,db_index=True)
    profile_qr=models.CharField(max_length=500,null=True,blank=True)
    registeration_number=models.CharField(max_length=300,blank=True,null=True)

    adhaar_card=models.FileField(upload_to="doctors_adhaar_card/",null=True,blank=True)
    registeration_card_image=models.FileField(upload_to="reg_cards/",null=True,blank=True)
    passport_size_image=models.FileField(upload_to="doctor_images/",null=True,blank=True)
    profile_pic=models.FileField(upload_to="profilepics/",default="profile_pics/default_pp.jpg")
    
    submitted_at=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.email
    

class DoctorAddress(models.Model):
    doctor=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    address_type=models.CharField(max_length=200,blank=True,null=True)
    address=models.TextField(null=True,blank=True)
    lat=models.FloatField(null=True,blank=True)
    lon=models.FloatField(null=True,blank=True)

    def __str__(self)->str:
        return self.doctor.first_name+self.address
    





