from authentication.models import CustomUser
from django.db.transaction import atomic
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse
import httpx
from rest_framework import status
from .models import DoctorProfile,DoctorAddress
from .serializers import DoctorProfileSerializer,DoctorAddressSerializer

DOCTOR_SERVER="http://localhost:7000/"
PATIENT_SERVER_URL="http://localhost:5000/"


@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def add_doctor_address(request):
    data=request.data
    user=request.user
    doctor_address=DoctorAddress.objects.create(doctor=user,address_type=data["address_type"],address=data["address"],lat=float(data["lat"]),lon=float(data["lon"]))
    profile:DoctorProfile=user.doctorprofile
    resp=httpx.post(DOCTOR_SERVER+"add_address",json={
    "doc_id": doctor_address.id,
    "document": {
        "user_id": user.id,
        "name": profile.name,
        "role": "doctor",
        "speciality": profile.speciality,
        "address": data["address"],
        "phone_number": profile.phone_number,
        "location": {
            "lat": data["lat"],
            "lon": data["lon"]
        }
    }
})
    return JsonResponse(resp.json(),status=resp.status_code)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_doctor_info(request):
    user=request.user
    data=DoctorProfileSerializer(user.doctorprofile).data
    return JsonResponse(data,status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_doctor_addresses(request):
    addresses=DoctorAddress.objects.filter(doctor=request.user)
    print(addresses)
    data=DoctorAddressSerializer(addresses,many=True).data
    print(data)
    return JsonResponse({"addresses":data,"count":len(data)},status=200)
    

    
@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def update_doctor_profile(request):
    data=request.data
    doctor=DoctorProfile.objects.get(user=request.user)
    for key,value in data.items():
        setattr(doctor,key,value)
    doctor.save()
    data=DoctorProfileSerializer(doctor).data
    return JsonResponse({"data":data},status=201)

@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def update_multi_media_data(request):
    try:
        multi_media_name=request.POST["mm_type"]
        doctor=DoctorProfile.objects.get(user=request.user)
        file=request.FILES["file"]
        if multi_media_name=="addhar":
            doctor.adhaar_card=file
        elif multi_media_name=="reg_card":
            doctor.registeration_card_image=file
        elif multi_media_name=="pp_image":
            doctor.passport_size_image=file
        elif multi_media_name=="profile_pic":
            doctor.profile_pic=file
        doctor.save()

        return JsonResponse({"mssg":"Update Successfull...."},status=201)
    except:
        return JsonResponse({"mssg":"Update Unsucessfull...."},status=400)
    



