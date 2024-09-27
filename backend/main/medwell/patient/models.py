from django.db import models
from authentication.models import CustomUser
import uuid

class PatientProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=200,blank=False,null=False)
    age = models.CharField(max_length=5,null=True,blank=True)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    blood_group=models.CharField(max_length=10,blank=True,null=True)
    city = models.CharField(max_length=100,null=True,blank=True)  
    country = models.CharField(max_length=100,null=True,blank=True) 
    state = models.CharField(max_length=100,null=True,blank=True) 
    pin = models.CharField(max_length=10,null=True,blank=True) 
    profile_pic=models.FileField(upload_to="profilepics/",null=True,blank=True)
    profile_qr=models.FileField(upload_to="user_qrs/",null=True,blank=True)
    adhaar_card=models.FileField(upload_to="addhaar_cards/",null=True,blank=True)

    
    def __str__(self) -> str:
        return self.user.email
    