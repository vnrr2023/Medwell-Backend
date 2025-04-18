from authentication.models import CustomUser
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse
from .models import *
from django.core.mail import send_mail
from .services import create_html
from .serializers import PatientSerializer
import datetime
from authentication.security import create_token,decrypt_json_string
from .models import RequestAccess
from .utils import create_qr,request_access

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
    pp=request.FILES["profile_pic"]
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

@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])   
def share_with_doctor(request):
    user=request.user
    payload={
        "user_id":user.id,
        "email":user.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
    }
    enc_token=create_token(payload)
    path=create_qr(enc_token,user.email)
    path="/"+"/".join(path.split("\\")[-3:])
    return JsonResponse(
        {"qr_code":path},status=200
    )


@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def provide_access(request):
    try:
        enc_string=request.data["enc_data"]
        data=int(decrypt_json_string(enc_string))
        doctor=CustomUser.objects.get(id=data)
        req_access=RequestAccess.objects.create(
            doctor=doctor,patient=request.user
            )
        request_access(data,request.user.id)
        return JsonResponse(data={"mssg":f"Request Granted to {doctor.first_name} Successfully..."},status=200)
    except Exception as e:
        print(e)
        return JsonResponse(data={"mssg":"Issue Granting Request..Please try again..."},status=400)

