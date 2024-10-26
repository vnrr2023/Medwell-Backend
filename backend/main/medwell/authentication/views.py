from django.conf import settings
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from .models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework import status
import requests
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
import random
from django.shortcuts import get_object_or_404
import datetime
from .security import decrypt_token,give_token_for_otp,give_enc_token
from django.core.mail import send_mail
from rest_framework.response import Response
from urllib.parse import unquote
from django.template.loader import render_to_string
from patient.models import PatientProfile
from django.core.files.base import ContentFile
from django.db.transaction import atomic

@api_view(["POST"])
@csrf_exempt
def login_with_google( request):
    token=request.POST["token"]
    if not token:
        return Response({"error": "Token not provided","status":False}, status=status.HTTP_400_BAD_REQUEST)
    try:
        id_info = id_token.verify_oauth2_token(token, google_requests.Request(), settings.GOOGLE_OAUTH2_CLIENT_ID)

        email = id_info['email']
        first_name = id_info.get('given_name', '')
        last_name = id_info.get('family_name', '')
        given_name = id_info.get('given_name', '')
        profile_pic_url = id_info.get('picture', '')
        

        user, created = CustomUser.objects.get_or_create(email=email, defaults={
            'first_name': first_name,
            'last_name': last_name,
            'email_verified':True,
            'profile_created':True,
        })

        if created:
            user.set_unusable_password()
            user.save()
            resp=requests.get(profile_pic_url)
            patient=PatientProfile()
            patient.name=first_name+last_name
            if resp.status_code==200:
                image_name = profile_pic_url.split("/")[-1]
                patient.profile_pic.save(image_name, ContentFile(resp.content))
            patient.save()
            html_content = render_to_string('welcome_google.html', {'email': email, 'profile_pic_url': profile_pic_url})
            send_mail(
                'Email Verification Medwell',
                    ' ', 
                settings.EMAIL_HOST_USER,
                [email], 
                html_message=html_content
                )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
            "access": str(refresh.access_token),
            "status":True
            }, 
        status=status.HTTP_200_OK
        )

    except ValueError as e:
        return Response({"error": "Invalid token","status":False}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@csrf_exempt
def login_user(request):
    email=request.POST['email']
    password=request.POST['password']
    user=authenticate(request,email=email,password=password)
    print(user)
    if user is None:
        return JsonResponse({'mssg':'Incorrct Credentials','status':0},status=status.HTTP_400_BAD_REQUEST)
    else:
        refresh=RefreshToken.for_user(user)
        access=refresh.access_token
        return JsonResponse(
            data={
                'access_token':str(access),
                'status':1
            },
            status=200
        )

@atomic
@api_view(['POST'])
@csrf_exempt
def register_user(request):
    email=request.POST['email']
    password1=request.POST['password1']
    password2=request.POST['password2']
    name=request.POST["full_name"]

    if password1==password2:
        try:
            new_user=CustomUser.objects.create_user(
                email=email,
                password=password1,
                profile_created=False,
                first_name=name
            )
            new_user.save()
            patient=PatientProfile.objects.create(name=name,user=new_user)
            patient.save()

            refresh=RefreshToken.for_user(new_user)
            access=refresh.access_token
            payload={
                'email':email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=2),
                'user_id':new_user.id

            }
            token=give_enc_token(payload)

            html_content = render_to_string('welcome_register.html', {'token': token})
            send_mail(
                'Email Verification Medwell',
                    ' ', 
                settings.EMAIL_HOST_USER,
                [email], 
                html_message=html_content
                )

            return JsonResponse(
                {
                    'mssg':"Profile created Successfully...",
                    'status':True,
                    'access_token':str(access)
                },
                status=201
            )

        except:
            return JsonResponse(
                {
                    'mssg':f"Try Logging in.'{email}' is already exists...",
                    'status':False
                },
                status=400
            )
    else:
        return JsonResponse(
            data={
                'mssg':"Passwords Dont Match ... Try Again",
                'status':False
            },
            safe=False,
            status=status.HTTP_400_BAD_REQUEST
            )
    
@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method=='POST':
        old=request.POST['old_password']
        new=request.POST['new_password']
        user=request.user
        if user.check_password(old): #if old password is correct
            user.set_password(new)
            user.save()
            access=str(RefreshToken.for_user(user).access)
            return JsonResponse({
                'status':True,
                'message':"Password Changed Successfully....",
                'new_access_token':access

            },
            status=status.HTTP_201_CREATED
            )
        else:
            return JsonResponse(
                {
                    'status':False,
                    'message':"Incorrect Previous Password.."
                },
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        

@csrf_exempt
@api_view(["POST"])     
def forgot_password(request):
    email=request.POST['email_of_user']
    user=get_object_or_404(CustomUser,email=email)
    otp=str(random.randint(100000,999999))
    payload = {
        'user_id': user.id,
        'email': user.email,
        'otp': otp,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    }
    token=give_token_for_otp(payload)
    html_message = render_to_string('otp_email_template.html', {'email': email, 'otp_number': otp})
    send_mail(
            'OTP for logging in to  Medwell',
                ' ', 
            settings.EMAIL_HOST_USER,
            [email], 
            html_message=html_message
            )
    
    return JsonResponse({
        'otp':otp,
        'token':token
    },safe=False,status=200)


@csrf_exempt
@api_view(['POST'])
def check_otp(request):
    otp=request.POST['otp']
    enc_token=request.POST['token']
    data=decrypt_token(enc_token)
    if data['status']:
        otp_real=data['payload']['otp']
        if otp==otp_real:
            email=data['payload']['email']
            user=CustomUser.objects.get(email=email)
            access_token=str(RefreshToken.for_user(user).access_token)

            return JsonResponse(
                {
                    'access_token':access_token,
                    'status':True,
                },
                status=status.HTTP_200_OK
            )
        else:
            return JsonResponse({
                'message':'OTP didnt matched....'
            },status=400)
            
    else:
        return JsonResponse({
            'message':'OTP expired...Try Again!!',
            'status':False
        },
        status=status.HTTP_400_BAD_REQUEST
        )
    

@csrf_exempt
@api_view(['GET'])
def verify_mail(request):
    enc_token= unquote(request.GET.get("token"))
    data=decrypt_token(enc_token)
    if data['status']:
        print("came")
        payload=data['payload']
        id=payload['user_id']
        user=CustomUser.objects.get(id=id)
        user.email_verified=True
        user.save()
        return HttpResponseRedirect('https://imedwell.vercel.app/')
    else:
        return HttpResponseRedirect('< Url of Page showing Verified Link Has Expired>')


@csrf_exempt
@api_view(['POST'])  
@permission_classes([IsAuthenticated])  
def create_new_verification_message(request):
    user=request.user
    payload={
        'email':user.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=2),
        'user_id':user.id

    }
    token=give_enc_token(payload)
    html_content = render_to_string('welcome_register.html', {'token': token})
    send_mail(
        'Email Verification Medwell',
            ' ', 
        settings.EMAIL_HOST_USER,
        [user.email], 
        html_message=html_content
        )
    return JsonResponse({'status':True,'mssg':f'Verification Link Sent to {user.email}'})

