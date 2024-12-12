import cv2
from ultralytics import YOLO
import logging
import os
# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка модели YOLOv8s
try:
    model = YOLO('yolov8s.pt')
    logger.info("Модель YOLOv8s успешно загружена.")
except Exception as e:
    logger.error(f"Ошибка при загрузке модели YOLOv8s: {e}")
    exit()

# Список целевых классов
TARGET_CLASSES = ['person', 'bird', 'cat', 'dog']

def detect_living_being(frame):
    """
    Функция для детекции живых существ на кадре.

    :param frame: np.array в формате BGR
    :return: (True/False, [список обнаруженных классов])
    """
    try:
        results = model.predict(frame, conf=0.3)
    except Exception as e:
        logger.error(f"Ошибка при предсказании модели: {e}")
        return False, []

    detected_classes = []
    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            class_name = model.names[cls_id]

            if class_name in TARGET_CLASSES:
                detected_classes.append(class_name)
                # Рисуем бокс
                box_xyxy = box.xyxy[0].cpu().numpy().astype(int)
                frame = cv2.rectangle(frame, (box_xyxy[0], box_xyxy[1]), (box_xyxy[2], box_xyxy[3]), (0, 255, 0), 2)
                cv2.putText(frame, class_name, (box_xyxy[0], box_xyxy[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

    if detected_classes:
        logger.info(f"Обнаруженные классы: {detected_classes}")
        # Показываем кадр с боксами
        cv2.imshow("Detections", frame)
        cv2.waitKey(0)
        return True, detected_classes
    else:
        logger.info("Живые существа не обнаружены.")
        return False, []

# Загрузим тестовое изображение из видео
video_path = "B:\\sisya_popka\\VID_20241212_024545.mp4"

if not os.path.isfile(video_path):
    logger.error(f"Файл не найден: {video_path}")
    exit()

cap = cv2.VideoCapture(video_path)
# ret, frame = cap.read()
# cap.release()
frame_count = 0
detected_any = False

while True:
    ret, frame = cap.read()
    if not ret:
        logger.info("Достигнут конец видеофайла или ошибка чтения кадра.")
        break

    frame_count += 1
    logger.info(f"Обработка кадра {frame_count}")

    detected, classes = detect_living_being(frame)
    if detected:
        detected_any = True
        # Останавливаем обработку после первого обнаружения
        break

cap.release()
cv2.destroyAllWindows()

if detected_any:
    logger.info("Тест завершён: обнаружено живое существо.")
else:
    logger.info("Тест завершён: живые существа не обнаружены.")