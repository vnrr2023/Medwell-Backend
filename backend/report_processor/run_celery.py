import os
os.system("celery -A celery_config.celery_app worker -l info -P gevent")