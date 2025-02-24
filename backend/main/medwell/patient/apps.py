from django.apps import AppConfig
import redis
from django.conf import settings
from colorama import Fore
# Connect to Redis (adjust host and port as needed)


class PatientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'patient'
    redis_client = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,password=settings.REDIS_PASS)
    if redis_client.ping():
        print(Fore.GREEN+"Redis is running"+Fore.WHITE)
    else:
        print(Fore.RED+"Redis failed to connect"+Fore.WHITE)
