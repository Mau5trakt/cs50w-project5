import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Rolalog.settings')
app = Celery('Rolalog')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(
    # Able to set the max interval in 7.0 days
    beat_max_loop_interval=604800,
    broker_connection_retry_on_startup = True
)

app.conf.beat_schedule = {
    'print_users_15m': {
        'task': 'music.tasks.print_users',
        'schedule': 20.0
            #crontab(minute='*/15') # Every minute: 0, 5, 30, 45
        #'schedule': 20.0

    }
}

# app.conf.broker_connection_retry_on_startup = True

app.autodiscover_tasks()