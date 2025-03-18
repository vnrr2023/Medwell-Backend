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
from .google_maps_utility import geocodeAddress

DOCTOR_SERVER="http://localhost:7000/"
PATIENT_SERVER_URL="http://localhost:5000/"



@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def add_doctor_address(request):
    data=request.data
    user=request.user
    # user=CustomUser.objects.get(id=int(data["id"]))
    address=data["address"]
    timings=data["timings"]
    geocoded_data=geocodeAddress(address)
    if geocoded_data["status"]==False:
        return JsonResponse({"mssg":"Address could not be added.Plz enter proper address"},status=status.HTTP_400_BAD_REQUEST)
    
    doctor_address=DoctorAddress.objects.create(
        doctor=user,
        address_type=data["address_type"],
        address=geocoded_data["formatted_address"],
        lat=float(geocoded_data["location"]["lat"]),
        lon=float(geocoded_data["location"]["lng"]),
        timings=timings
        )
    profile:DoctorProfile=user.doctorprofile
#     resp=httpx.post(DOCTOR_SERVER+"add_address/",json={
#     "doc_id": doctor_address.id,
#     "document": {
#         "user_id": user.id,
#         "name": profile.name,
#         "role": "doctor",
#         "speciality": profile.speciality,
#         "address": doctor_address.address,
#         "phone_number": profile.phone_number,
#         "location": {
#             "lat": doctor_address.lat,
#             "lon":doctor_address.lon
#         }
#     }
# })
    # return JsonResponse(resp.json(),status=resp.status_code)
    return JsonResponse({"ok":"ok"},status=200)

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
    data=DoctorAddressSerializer(addresses,many=True).data
    return JsonResponse({"addresses":data,"count":len(data)},status=200)
    
    
@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def update_doctor_profile(request):
    data=request.data
    # user=CustomUser.objects.get(id=int(data["id"]))
    # del data["id"]
    user=request.user
    doctor=DoctorProfile.objects.get(user=user)
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
        if multi_media_name=="aadhaar":
            doctor.adhaar_card=file
        elif multi_media_name=="reg_card":
            doctor.registeration_card_image=file
        elif multi_media_name=="pp_image":
            doctor.passport_size_image=file
        elif multi_media_name=="profile_pic":
            doctor.profile_pic=file
        doctor.save()
        data=DoctorProfileSerializer(doctor).data
        return JsonResponse({"mssg":"Update Successfull....","data":data},status=201)
    except Exception as e:
        return JsonResponse({"mssg":"Update Unsucessfull...."},status=400)
    



