
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse
import httpx
from rest_framework import status
from patient.utils import check_access
from patient.models import RequestAccess,Report
from .serializers import RequestAccessSerializer
from patient.serializers import GetReportsSerializer
# Create your views here.

ANALYTICS_SERVICE=""

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def refresh_patients(request):
    user=request.user
    data=RequestAccessSerializer(RequestAccess.objects.filter(doctor=user).order_by("-requested_at"),many=True).data
    return JsonResponse(data,safe=False)

@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_patient_reports(request):
    user=request.user
    patient_id=request.data["patient_id"]
    if check_access(doctor_id=user.id,patient_id=patient_id):
        data=GetReportsSerializer(Report.objects.filter(user__id=int(patient_id)),many=True).data
        return JsonResponse(data,safe=False)
    return JsonResponse({"mssg":"Expired"},status=406)

    
@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_patient_health_check(request):
    user=request.user
    patient_id=request.data["patient_id"]
    if check_access(doctor_id=user.id,patient_id=patient_id):
        resp = httpx.post(
            f"{ANALYTICS_SERVICE}/doctor/patient-health-check/{patient_id}",
            json={"user_id": user.id}
        )
        print(resp.json(),resp.status_code)
        if resp.status_code==200 or resp.status_code==204:
            return JsonResponse(data=resp.json(),status=resp.status_code)
        return JsonResponse({"mssg":"Some Error Ocurred.."},status=400)
    return JsonResponse({"mssg":"Expired"},status=status.HTTP_406_NOT_ACCEPTABLE)

