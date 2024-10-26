from authentication.models import CustomUser
from django.db.transaction import atomic
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse
from rest_framework import status
from .models import *
from django.core.mail import send_mail
from .services import create_html
import httpx
from .serializers import PatientSerializer

AI_SERVER_URL="http://localhost:8888/"
PATIENT_SERVER_URL="http://127.0.0.1:5000/"
SELF_URL="http://localhost:8000/"

@api_view(["POST"])
@csrf_exempt
def send_status_of_task_to_mail(request):
    data=request.data
    user_id=data.get("user_id")
    status=data.get("status")
    pdf_file=data.get("pdf_file")
    email=CustomUser.objects.get(id=int(user_id)).email
    html_template=create_html(email,pdf_file,status)
    send_mail(
        subject='Your Medwell Report Processing Status',
        message='',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        html_message=html_template
    )
    return JsonResponse({'mssg':"mail sent"},status=200)


@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def health_check(request):
    user=request.user
    resp = httpx.post(
            f"{PATIENT_SERVER_URL}get_health_check/",
            json={"user_id": user.id}
        )
    print(resp.json(),resp.status_code)
    if resp.status_code==200 or resp.status_code==204:
        return JsonResponse(data=resp.json(),status=resp.status_code)
    return JsonResponse(data={},status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def save_patient_info(request):
    data=request.data
    patient=PatientProfile.objects.get(user=request.user)
    for key, value in data.items():
        setattr(patient, key, value)
    patient.save()

    patient_data=PatientSerializer(patient).data
    return JsonResponse(data=patient_data,safe=False,status=201)
    
@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def update_profile_pic(request):
    pp=request.POST.FILES["profile_pic"]
    patient=PatientProfile.objects.get(user=request.user)
    patient.profile_pic=pp
    patient.save()
    return JsonResponse(data={"message":"Profile Pic Updated Successfully...."},status=200)

@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_patient_info(request):
    user=request.user
    data=PatientSerializer( PatientProfile.objects.get(user=user)).data
    return JsonResponse(
        data=data,safe=False,status=200
    )

    

