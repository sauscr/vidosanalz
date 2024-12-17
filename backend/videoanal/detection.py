import cv2, os, torch

import numpy as np
from ultralytics import YOLO
import logging
# import face_recognition
# Предположим, что YOLO модель уже загружена:
# Обратите внимание: вам нужно подготовить веса YOLO: yolov5s.pt или yolov8s.pt
# и убедиться, что эта модель есть в вашем окружении.
#model = torch.hub.load('ultralytics/yolov8', 'yolov8s', pretrained=True)

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

try:
    model = YOLO('yolov8s.pt')  # Автоматически скачает весы, если их нет локально. Можно так же использовать GPU или CPU YOLO('yolov8s.pt', device='cuda')
    logger.info("Модель YOLOv8s успешно загружена.")#                                                                     YOLO('yolov8s.pt', device='cpu')
except Exception as e:
    logger.error(f"Ошибка при загрузке модели YOLOv8s: {e}")
    model = None

# Список классов YOLOv5 (примерно): ['person', 'bicycle', ...]
# Нас интересуют живые существа - например, 'person', 'bird', 'cat', 'dog'.
TARGET_CLASSES = ['person', 
                  #'bird', 
                  'cat', 
                  #'dog',
                  ]

# # Минимальная площадь объекта для фильтрации
# MIN_AREA = 500

# # Путь к каталогу с известными лицами сотрудников
# KNOWN_FACES_DIR = os.path.join(os.path.dirname(__file__), 'known_faces')

# # Словарь для хранения кодировок известных лиц
# KNOWN_FACE_ENCODINGS = {}
# KNOWN_FACE_NAMES = []

# def load_known_faces():
    # """
    # Загрузка изображений известных лиц сотрудников и вычисление их кодировок.
    # """
    # global KNOWN_FACE_ENCODINGS, KNOWN_FACE_NAMES
    # if not os.path.exists(KNOWN_FACES_DIR):
    #     logger.error(f"Каталог с известными лицами не найден: {KNOWN_FACES_DIR}")
    #     return

    # for filename in os.listdir(KNOWN_FACES_DIR):
    #     if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
    #         path = os.path.join(KNOWN_FACES_DIR, filename)
    #         image = face_recognition.load_image_file(path)
    #         encodings = face_recognition.face_encodings(image)
    #         if encodings:
    #             KNOWN_FACE_ENCODINGS[filename] = encodings[0]
    #             # Извлекаем имя сотрудника из имени файла
    #             name = os.path.splitext(filename)[0].replace('_', ' ').title()
    #             KNOWN_FACE_NAMES.append(name)
    #             logger.info(f"Загружено лицо: {name}")
    #         else:
    #             logger.warning(f"Не удалось обнаружить лицо на изображении: {filename}")

# Загрузка известных лиц при импорте модуля
# load_known_faces()

def detect_living_being(frame, output_path=None):
    """
    Функция для детекции живых существ на кадре с сохранением результатов.

    :param frame: np.array в формате BGR
    :param output_path: путь для сохранения кадра с нанесенными детекциями
    :return: True, если обнаружено живое существо, иначе False и список обнаруженных классов
    """
    if model is None:
        logger.error("Модель YOLOv8s не загружена.")
        return False, [], 0.0

    try:
        # Установим порог уверенности (conf) и NMS
        results = model.predict(frame, conf=0.5, iou=0.45)
    except Exception as e:
        logger.error(f"Ошибка при предсказании модели: {e}")
        return False, [], 0.0

    detected_classes = []
    confidences = []
    if results and results[0].boxes.data.shape[0] > 0:  # Если есть детекции
        for box in results[0].boxes.data:
            x1, y1, x2, y2, conf, cls_id = box[:6].tolist()
            conf = float(conf)
            cls_id = int(cls_id)

            # Фильтруем по порогу уверенности и интересующим классам
            class_name = model.names[cls_id]
            if conf > 0.3 and class_name in TARGET_CLASSES:
                detected_classes.append(class_name)
                confidences.append(conf)

                # Рисуем рамки и метки на кадре
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                label = f"{class_name} {conf:.2f}"
                cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Сохраняем кадр с детекциями, если задан путь
        if output_path:
            cv2.imwrite(output_path, frame)
            logger.info(f"Кадр с детекциями сохранен по пути: {output_path}")

    if detected_classes:
        logger.info(f"Обнаруженные классы: {', '.join(detected_classes)}")
        average_conf = np.mean(confidences)
        logger.info(f"Средний коэффициент доверенности: {average_conf:.2f}")
        return True, detected_classes, average_conf
    else:
        logger.info("Живые существа не обнаружены.")
        return False, [], 0.0

def delete_frame_if_low_confidence(frame_path, average_conf, threshold=0.75):
    """
    Удаляет кадр, если средний коэффициент доверенности всех детекций меньше заданного порога.

    :param frame_path: Путь к изображению кадра.
    :param average_conf: Средний коэффициент доверенности.
    :param threshold: Порог уверенности для удаления кадра.
    """
    if average_conf < threshold:
        if os.path.exists(frame_path):
            try:
                os.remove(frame_path)
                logger.info(f"Кадр удалён из-за низкой уверенности ({average_conf:.2f}): {frame_path}")
            except Exception as e:
                logger.error(f"Ошибка при удалении кадра {frame_path}: {e}")
    else:
        logger.info(f"Кадр сохранён. Средний коэффициент доверенности ({average_conf:.2f}) выше порога ({threshold}).")