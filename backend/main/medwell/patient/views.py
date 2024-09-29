from authentication.models import CustomUser
from django.db.transaction import atomic
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse
from rest_framework import status
import json
import requests
from .models import *
from django.shortcuts import get_object_or_404
import datetime
from django.core.mail import send_mail
from rest_framework.response import Response
from .services import create_html

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
    print(report.report_file.url)
    data={'file':SELF_URL+report.report_file.url,"user_id":str(user.id),"report_id":str(report.id)}
    resp=requests.post(AI_SERVER_URL+"process_report/",json=data)
    task_id=resp.json()['task_id']
    return JsonResponse(
        {
            'task_id':task_id
        },status=200
    )

@api_view(["POST"])
@csrf_exempt
def send_status_of_task(request):
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