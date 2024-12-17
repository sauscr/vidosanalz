import os
from celery import Celery
import logging
# from celery. import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config', broker='redis://localhost:6379/1',
             backend='redis://localhost:6379/1', include=['videoanal.tasks'])


# Настройка логирования
celery_logger = logging.getLogger('celery')

# Настроим уровень логирования
celery_logger.setLevel(logging.INFO)

# Добавим обработчик для вывода логов в терминал
if not celery_logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(processName)s] %(message)s')
    handler.setFormatter(formatter)
    celery_logger.addHandler(handler)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')