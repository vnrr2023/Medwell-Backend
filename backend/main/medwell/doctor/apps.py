from django.apps import AppConfig
# import redis

class DoctorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'doctor'
    # redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
