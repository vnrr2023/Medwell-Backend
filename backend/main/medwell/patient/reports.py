from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse
from rest_framework import status
import requests
from .models import *
from .serializers import GetReportsSerializer
from .apps import PatientConfig
from celery.result import AsyncResult

@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def send_report(request):
    print(request.FILES)
    pdf_file=request.FILES['report']
    user:CustomUser=request.user
    report=Report.objects.create(user=user,report_file=pdf_file)
    report.save()
    task = PatientConfig.celery_app.send_task("tasks.process_pdf", args=[report.report_file.url,str(report.id),str(user.id),user.email,user.first_name])
    return JsonResponse({'task_id':task.id},status=200)



@api_view(["GET"])
def get_task_status(request,task_id):
    task_result = AsyncResult(task_id, app=PatientConfig.celery_app)
    if task_result.state == 'PENDING':
        response = {
            "state": task_result.state,
            "status": "Pending..."
        }
    elif task_result.state == 'STARTED':
        response = {
            "state": task_result.state,
            "status": "In progress..."
        }
    elif task_result.state == 'SUCCESS':
        response = {
            "state": task_result.state,
            "result": task_result.result
        }
    elif task_result.state == 'FAILURE':
        response = {
            "state": task_result.state,
            "status": str(task_result.info) 
        }
    else:
        response = {
            "state": task_result.state,
            "status": "Unknown state"
        }
    return JsonResponse(response,status=200)

@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_reports(request):
    user=request.user
    reports=Report.objects.filter(user=user).order_by("-submitted_at")
    if reports:
        data=GetReportsSerializer(reports,many=True).data
        return JsonResponse(
            data={"reports":data,"count":len(reports)},status=status.HTTP_200_OK
        )
    return JsonResponse(data={"count":0},status=status.HTTP_204_NO_CONTENT)


# @api_view(["POST"])
# @csrf_exempt
# @permission_classes([IsAuthenticated])
# def create_agent(request):
#     user=request.user
#     resp=requests.post(CHATBOT_URL+"create_agent",json={"user_id":user.id,"email":user.email})
#     return JsonResponse(resp.json(),status=resp.status_code)


# @api_view(["POST"])
# @csrf_exempt
# def chat_with_reports(request):
#     data=request.data
#     resp=requests.post(CHATBOT_URL+"chat",json={"key":data["key"],"question":data["question"]})
#     return JsonResponse(resp.json(),status=resp.status_code)
