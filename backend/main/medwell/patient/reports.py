from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse
from rest_framework import status
import requests
from .models import *
from .serializers import GetReportsSerializer

AI_SERVER_URL="http://localhost:8888/"
SELF_URL="http://localhost:8000/"

@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def send_report(request):
    pdf_file=request.FILES['report']
    user=request.user
    report=Report.objects.create(user=user,report_file=pdf_file)
    report.save()
    data={'file':SELF_URL+report.report_file.url,"user_id":str(user.id),"report_id":str(report.id)}
    resp=requests.post(AI_SERVER_URL+"process_report/",json=data)
    task_id=resp.json()['task_id']
    return JsonResponse(
        {
            'task_id':task_id
        },status=200
    )



@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_report_task_status(request):
    task_id=request.GET["task_id"]
    resp=requests.get(AI_SERVER_URL+f"get_task_status/?task_id={task_id}").json()
    print(resp)
    return JsonResponse(data={
        "status":resp["state"]
    },safe=False)

@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_reports(request):
    user=request.user
    reports=Report.objects.filter(user=user).order_by("-date_of_report")
    if reports:
        data=GetReportsSerializer(reports,many=True).data
        return JsonResponse(
            data={"reports":data,"count":len(reports)},status=status.HTTP_200_OK
        )
    return JsonResponse(data={"count":0},status=status.HTTP_204_NO_CONTENT)



