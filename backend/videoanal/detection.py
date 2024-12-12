import torch
import cv2
import numpy as np
from ultralytics import YOLO
import logging
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
TARGET_CLASSES = ['person', 'bird', 'cat', 'dog']

def detect_living_being(frame):
    # # frame - это np.array (BGR) от OpenCV
    # # Преобразуем BGR -> RGB
    # img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # results = model(img, size=640)
    # # results.xyxy[0] - детекции [x1,y1,x2,y2,conf,class]
    # for *box, conf, cls in results.xyxy[0].cpu().detach().numpy():
    #     class_name = results.names[int(cls)]
    #     if class_name in TARGET_CLASSES and conf > 0.5:
    """
    Функция для детекции живых существ на кадре.

    :param frame: np.array в формате BGR
    :return: True, если обнаружено живое существо, иначе False
    """
    # YOLOv8 принимает кадр в формате BGR
    if model is None:
        logger.error("Модель YOLOv8s не загружена.")
        return False, []

    try:
        # YOLOv8 принимает кадр в формате BGR
         results = model.predict(frame, conf=0.3, iou=0.45)  # Устанавливаем пороги уверенности и NMS
        #  results = model(frame)  # Получение результатов от модели
         print("Результаты детекции:", results)

    except Exception as e:
        logger.error(f"Ошибка при предсказании модели: {e}")
        return False, []
    
    detected_classes = []
    if results:
        # for result in results:
        #     for box in result.boxes:
        #         cls_id = int(box.cls[0])
        #         class_name = model.names[cls_id]

        #         if class_name in TARGET_CLASSES:
        #             detected_classes.append(class_name)
        # Результаты могут быть в виде списка, в котором каждый элемент — это объект
        for result in results[0].boxes.data:  # Применяем для первого кадра. result[x] - проверяет каждый x-й кадр
            if result[4] > 0.1:  # Если уверенность > 0.5; поигрался с коэффициэнтом уверенности
                detected_classes.append(result[5])  # Добавляем имя класса (последний индекс)
    
    # for result in results:
    #     for box in result.boxes:
    #         cls_id = int(box.cls[0])
    #         class_name = model.names[cls_id]
    #         if class_name in TARGET_CLASSES:
    #             return True
    if detected_classes:
        logger.info(f"Обнаруженные классы: {detected_classes}")
        return True, detected_classes
    else:
        logger.debug("Живые существа не обнаружены.")
        return False, []
