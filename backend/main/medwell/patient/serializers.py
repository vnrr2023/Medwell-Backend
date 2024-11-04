# serializers.py
from rest_framework import serializers
from .models import PatientProfile,Report,ReportDetail
from authentication.models import CustomUser
class ReportDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=ReportDetail
        fields=[
            "report_data"

        ]

class GetReportsSerializer(serializers.ModelSerializer):
    reportdetail = ReportDetailSerializer(read_only=True)
    class Meta:
        model=Report
        fields=[
            'id','report_file','report_type','submitted_at','date_of_collection','doctor_name','date_of_report','summary','reportdetail'
        ]

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=[
            "id",
            "email"

        ]

class PatientSerializer(serializers.ModelSerializer):
    user_info = CustomUserSerializer(source='user', read_only=True)
    class Meta:
        model=PatientProfile
        fields = [
            'id',
            'name',
            'age',
            'phone_number',
            'user_info',
            'blood_group',
            'city',
            'country',
            'state',
            'pin',
            'profile_pic',
            'profile_qr',
            'adhaar_card',
            'allergies',
            'chronic_conditions',
            'family_history',
            'health_summary',
            'diet_plan'
        ]
