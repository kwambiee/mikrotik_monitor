import os
from celery.schedules import crontab
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mikrotik_monitor.settings')

app = Celery('mikrotik_monitor')
app.config_from_object('django.conf:settings', namespace='CELERY')
print("----about to load the task.... ")
app.conf.beat_schedule = {
    'update-router-list': {
        'task': 'routers.tasks.update_router_list',
        'schedule': crontab(minute='*/30'), 
    },
}

app.autodiscover_tasks()

# Explicit broker setting
app.conf.broker_url = os.getenv('CELERY_BROKER_URL')
