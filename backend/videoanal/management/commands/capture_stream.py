from django.core.management.base import BaseCommand
import cv2
import time
import os
from django.conf import settings
from videoanal.tasks import analyze_frame_task
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class Command(BaseCommand):
    help = 'Capture frames from RTSP stream and send them for analysis.'

    def add_arguments(self, parser):
        parser.add_argument('--url', type=str, help='Video stream URL или путь к видеофайлу', required=True)
        parser.add_argument('--interval', type=int, help='Seconds between frames', default=5)
        parser.add_argument('--source_type', type=str, choices=['stream', 'file'], default='stream',
                            help='Тип источника: "stream" для RTSP или HTTP-потока, "file" для видеофайла')

    def handle(self, *args, **options):
        source = options['url']
        interval = options['interval']
        source_type = options['source_type']

        if source_type == 'stream':
            cap = cv2.VideoCapture(source)
            source_desc = f"стрим {source}"
        elif source_type == 'file':
            if not os.path.isfile(source):
                logger.error(f"Файл не найден: {source}")
                return
            cap = cv2.VideoCapture(source)
            source_desc = f"видео файл {source}"
        else:
            logger.error(f"Неизвестный тип источника: {source_type}")
            return

        if not cap.isOpened():
            logger.error(f"Не удалось открыть источник: {source_desc}")
            return

        logger.info(f"Начало захвата кадров из {source_desc}")
        last_capture = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                if source_type == 'file':
                    logger.info("Достигнут конец видеофайла. Завершение захвата.")
                    break
                else:
                    logger.error("Кадр не получен. Попытка переподключения...")
                    cap.release()
                    time.sleep(5)  # Подождать перед повторным подключением
                    cap = cv2.VideoCapture(source)
                    if not cap.isOpened():
                        logger.error(f"Не удалось переподключиться к источнику: {source_desc}")
                        break
                    continue

            current_time = time.time()
            if current_time - last_capture >= interval:
                # Сохранение кадра
                daily_dir = os.path.join(settings.MEDIA_ROOT, 'frames', datetime.now().strftime('%Y-%m-%d'))
                os.makedirs(daily_dir, exist_ok=True)
                filename = datetime.now().strftime("%H%M%S%f") + ".jpg"
                frame_path = os.path.join(daily_dir, filename)
                cv2.imwrite(frame_path, frame)

                # Отправка задачи Celery
                analyze_frame_task.delay_on_commit(frame_path)
                logger.info(f"Захвачен и отправлен кадр: {frame_path}")

                last_capture = current_time

        cap.release()
        logger.info("Захват кадров завершён.")