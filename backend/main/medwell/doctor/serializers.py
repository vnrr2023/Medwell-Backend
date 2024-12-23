from rest_framework import serializers
from patient.models import RequestAccess
from authentication.models import CustomUser
from .models import DoctorAddress,DoctorProfile

class UserSerializer(serializers.ModelSerializer):
       class Meta:
        model=CustomUser
        fields=[
            "id",
            "email"

        ]
    
class DoctorProfileSerializer(serializers.ModelSerializer):
    doctor_info = UserSerializer(source='user', read_only=True)
    class Meta:
        model=DoctorProfile
        fields=["doctor_info","name","phone_number","dob","speciality","verified","profile_qr","registeration_number","adhaar_card","registeration_card_image","passport_size_image","profile_pic","submitted_at"]



class RequestAccessSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='patient', read_only=True)
    class Meta:
        model=RequestAccess
        fields=[
            "requested_at","user_info"
        ]



class DoctorAddressSerializer(serializers.ModelSerializer):
    doctor_info = UserSerializer(source='doctor', read_only=True)
    class Meta:
        model=DoctorAddress
        fields=["address_type","address","lat","lon","doctor_info"]
        