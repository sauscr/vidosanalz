from pathlib import Path
from celery import shared_task
import cv2
from django.conf import settings
from django.core.files import File
from django.utils import timezone
from django.core.management import call_command
import os
from .models import Event
from .detection import detect_living_being
from .telegram_utils import send_telegram_message, send_telegram_photo
import logging

# Event.objects.get(pk=1)
# Event.refresh_from_db()

# Настройка логирования
logger = logging.getLogger('celery')
logger.setLevel(logging.INFO)

# Создаем консольный обработчик, если он ещё не добавлен
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

@shared_task
def analyze_frame_task(frame_path):
    frame_path = Path(frame_path)
    abs_frame_path = settings.MEDIA_ROOT / frame_path
    logger.info(f"Начало анализа кадра: {frame_path}")
    if not os.path.exists(abs_frame_path):
        logger.error(f"Файл кадра не найден: {frame_path}")
        return

    frame = cv2.imread(abs_frame_path)
    if frame is None:
        logger.error(f"Не удалось прочитать кадр: {frame_path}")
        return

    # Анализируем кадр с сохранением обработанного изображения # identified_employees 
    detected, detected_classes, average_conf = detect_living_being(frame, output_path=frame_path)
    
    

    if detected:
        # Формируем описание с обнаруженными классами
        # Преобразуем имена классов в удобочитаемый формат (например, с заглавной буквой)
        detected_classes_readable = [cls.capitalize() for cls in detected_classes]
        classes_str = ', '.join(detected_classes_readable)
        description = f"Обнаружены живые существа: {classes_str}."

         # Если есть идентифицированные сотрудники, добавляем их в описание
        # if identified_employees:
        #     # Убираем дубликаты и сортируем
        #     identified_employees = sorted(list(set(identified_employees)))
        #     employees_str = ', '.join(identified_employees)
        #     description = f"Обнаружены живые существа: {classes_str}. Идентифицированные сотрудники: {employees_str}."
        # else:
        #     description = f"Обнаружены живые существа: {classes_str}. Сотрудники не идентифицированы."


        # Создаём Event в БД
        
        # frame_path = frame_path.replace(str(settings.MEDIA_ROOT) + '/', '')
        
              
        event = Event.objects.create(
            image=frame_path,
            description=description  # Обновленное описание
        )

        # Логируем событие
        message = f"{description} в {event.timestamp.strftime('%d-%m-%Y %H:%M:%S')}."
        logger.info(message)

        # Добавляем классы детекций в лог (можно убрать, если уже включено в `message`)
        logger.info(f"Классы обнаруженных объектов: {classes_str}")

        # # Сохраняем обработанный кадр с детекциями
        # output_dir = os.path.join(settings.MEDIA_ROOT, 'processed_frames')
        # os.makedirs(output_dir, exist_ok=True)
        # output_path = os.path.join(output_dir, os.path.basename(frame_path))
        # cv2.imwrite(output_path, frame)
        # logger.info(f"Кадр с детекциями сохранен: {output_path}")

        cv2.imwrite(abs_frame_path, frame)
        logger.info(f"Кадр с детекциями сохранен: {abs_frame_path}")

        # Отправляем уведомление и фото в Telegram
        send_telegram_message(message)
        send_telegram_photo(abs_frame_path)

    else:
        # Если нет обнаружений, удаляем кадр
        try:
            os.remove(abs_frame_path)
            logger.debug(f"Кадр удалён, детекция не удалась: {abs_frame_path}")
        except Exception as e:
            logger.error(f"Ошибка при удалении кадра {abs_frame_path}: {e}")

    logger.info(f"Завершён анализ кадра: {abs_frame_path}")