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
    education=models.CharField(max_length=500,null=True,blank=True)
    
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
    timings=models.JSONField(null=True,blank=True)

    def __str__(self)->str:
        return self.doctor.first_name+self.address
    

class DoctorServices(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid4, editable=False)
    doctor=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    service_name=models.CharField(max_length=300,null=True,blank=True)
    service_amount=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.doctor.first_name
    

class AppointmentSlot(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid4, editable=False)
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="appointment_slots")
    address=models.ForeignKey(DoctorAddress,on_delete=models.CASCADE,related_name="appointment_address",null=True,blank=True)
    timing = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    class Meta:
        indexes=[
           
            models.Index(fields=["doctor","status"]),
            models.Index(fields=["doctor","date"]),
        ]


    def __str__(self):
        return self.doctor.first_name


class Appointment(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid4, editable=False)
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="appointments")
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="appointments_as_patient")
    service = models.ForeignKey(DoctorServices, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    appointment_slot = models.ForeignKey(AppointmentSlot, on_delete=models.CASCADE)


    class Meta:
        indexes=[
            models.Index(fields=["doctor","patient"])
        ]

    def __str__(self):
        return self.doctor.first_name + " " + self.patient.first_name + " " + str(self.booked_at)


class AppointmentPayment(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid4, editable=False)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(max_length=200, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.appointment.doctor.first_name


class ServiceMarketting(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    doctor=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    html=models.TextField(null=True,blank=True)


    def __str__(self):
        return self.doctor.first_name+" "+self.id        






