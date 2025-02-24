from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse
from rest_framework import status
import requests
from .models import *
from .serializers import GetReportsSerializer

AI_SERVER_URL="http://localhost:8888/"
CHATBOT_URL="http://localhost:6000/"

@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def send_report(request):
    print(request.FILES)
    pdf_file=request.FILES['report']
    user=request.user
    report=Report.objects.create(user=user,report_file=pdf_file)
    report.save()
    data={'file':report.report_file.url,"user_id":str(user.id),"report_id":str(report.id),"email":user.email,"name":user.first_name}
    resp=requests.post(AI_SERVER_URL+"process_report",json=data)
    task_id=resp.json()['task_id']
    return JsonResponse(
        {
            'task_id':"task_id"
        },status=200
    )



# @api_view(["GET"])
# @csrf_exempt
# def get_report_task_status(request):
#     task_id=request.GET["task_id"]
#     resp=requests.get(AI_SERVER_URL+f"get_task_status/{task_id}").json()
#     print(resp)
#     return JsonResponse(data={
#         "status":resp["state"]
#     },safe=False)

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


@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def create_agent(request):
    user=request.user
    resp=requests.post(CHATBOT_URL+"create_agent",json={"user_id":user.id,"email":user.email})
    return JsonResponse(resp.json(),status=resp.status_code)


@api_view(["POST"])
@csrf_exempt
def chat_with_reports(request):
    data=request.data
    resp=requests.post(CHATBOT_URL+"chat",json={"key":data["key"],"question":data["question"]})
    return JsonResponse(resp.json(),status=resp.status_code)
