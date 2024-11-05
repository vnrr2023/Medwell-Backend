from django.apps import AppConfig
import redis

# Connect to Redis (adjust host and port as needed)


class PatientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'patient'
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
