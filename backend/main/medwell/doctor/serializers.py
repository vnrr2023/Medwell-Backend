from rest_framework import serializers
from patient.models import RequestAccess
from authentication.models import CustomUser

class PatientSerilizerData(serializers.ModelSerializer):
       class Meta:
        model=CustomUser
        fields=[
            "id",
            "email"

        ]
    


class RequestAccessSerializer(serializers.ModelSerializer):
    user_info = PatientSerilizerData(source='patient', read_only=True)
    class Meta:
        model=RequestAccess
        fields=[
            "requested_at","user_info"
        ]
