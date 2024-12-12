from celery import shared_task
import cv2
from django.conf import settings
from django.core.files import File
from django.utils import timezone
import os
from .models import Event
from .detection import detect_living_being
from .telegram_utils import send_telegram_message, send_telegram_photo
import logging

#Настройка логирования
logger = logging.getLogger('celery')
logger.setLevel(logging.INFO)

#СОздаем консольный обработчик, если он ещё не добавлен
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

@shared_task
def analyze_frame_task(frame_path):
    logger.info(f"Начало анализа кадра: {frame_path}")
    # frame_path - абсолютный путь к файлу кадра
    if not os.path.exists(frame_path):
        logger.error(f"Файл кадра не найден: {frame_path}")
        return

    frame = cv2.imread(frame_path)
    if frame is None:
        logger.error(f"Не удалось прочитать кадр: {frame_path}")
        return

    # Анализируем кадр
    detected, detected_classes = detect_living_being(frame)

    if detected:
        # Создаём Event в БД
        relative_path = frame_path.replace(str(settings.MEDIA_ROOT) + '/', '')
        event = Event.objects.create(
            image=relative_path,
            description='Обнаружено живое существо'
        )

        #логируем Event в терминал
        message = f"Обнаружено движение живого существа в {event.timestamp.strftime('%d-%m-%Y %H:%M:%S')}."
        logger.info(message)
        logger.info(f"Кадр сохранён: {frame_path}")
        logger.info(f"Классы обнаруженных объектов: {', '.join(detected_classes)}")
        # Отправляем уведомление в Telegram
        send_telegram_message(message)
        send_telegram_photo(frame_path)

    else:
        # Если нет обнаружения, можно удалить кадр, чтобы не засорять хранилище
        try:
            os.remove(frame_path)
            logger.debug(f"Кадр удалён, детекция не удалась: {frame_path}")
        except Exception as e:
            logger.error(f"Ошибка при удалении кадра {frame_path}: {e}")
    logger.info(f"Завершён анализ кадра: {frame_path}")