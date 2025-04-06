
from pathlib import Path
import os
import environ
import requests

BASE_DIR = Path(__file__).resolve().parent.parent
env=environ.Env()
env_file_path=os.path.join(BASE_DIR, '.env')
environ.Env.read_env(env_file_path)


SECRET_KEY = env("SECRET_KEY")
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'patient',
    'authentication',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'doctor',
    "storages"
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'medwell.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'medwell.wsgi.application'
X_FRAME_OPTIONS = 'ALLOWALL' 


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("DB_NAME"),         
        'USER': env("USER"),             
        'PASSWORD': env("PASSWORD"),     
        'HOST': env("DB_HOST"),          
        'PORT': env("DB_PORT"),                 
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
AUTH_USER_MODEL = 'authentication.CustomUser'
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "ngrok-skip-browser-warning" 
)

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True



STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Rest framework Configuration

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=50),
    'ALGORITHM': 'HS256'

}

REST_FRAMEWORK = {
    
    'DEFAULT_AUTHENTICATION_CLASSES': (
        
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
    
}

# Google OAuth Config
GOOGLE_OAUTH2_CLIENT_ID = env("GOOGLE_OAUTH2_CLIENT_ID")
GOOGLE_OAUTH2_CLIENT_SECRET = env("GOOGLE_OAUTH2_CLIENT_SECRET")
GOOGLE_MAPS_SECRET=env("GOOGLE_MAPS_SECRET")

EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER=env('EMAIL')
EMAIL_HOST_PASSWORD=env('EMAIL_PASSWORD')
EMAIL_USE_TLS=True

REDIS_HOST=env("REDIS_HOST")
REDIS_PORT=int(env("REDIS_PORT"))
REDIS_PASS=env("REDIS_PASS")


REDIS_URI=env("REDIS_URI")

AWS_ACCESS_KEY_ID=env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY=env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME=env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN="%s.s3.amazonaws.com"% AWS_STORAGE_BUCKET_NAME
AWS_S3_FILE_OVERWRITE=False

STORAGES = {
 
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
    },
    

    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
    },
}

service_urls = {
    "GMAPS_SERVICE": "https://gmapsmedwell.vercel.app/",
    "DOCTOR_SEARCH_SERVICE": "https://doctor-search-medwell.vercel.app/",
    # "ANALYTICS_SERVICE": "",
    "MESSAGING_SERVICE": "https://whatsapp-messaging-medwell-api.vercel.app/test"
}

# Check each URL
for name, url in service_urls.items():
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            print(f"{name}: ✅ Service is up")
        else:
            print(f"{name}: ❌ Service is down")
        print()
    except Exception as e:
        print(f"{name}: ❌ Error occurred - {e}")

