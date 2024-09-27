from django.urls import path
from .views import *
urlpatterns = [
    path("google_login/",login_with_google,name="google_login"),
    path('login_user',login_user,name='login_user'),
    path('register_user',register_user,name='register_user'),
    # path('change_password',change_password,name='change_password'),
    # path('forgot_password',forgot_password,name='forgot_password'),
    # path('check_otp',check_otp,name='check_otp'),
    path('verify_mail/',verify_mail,name='verify_mail'),

]
