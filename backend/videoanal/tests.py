import base64, logging, os, django
from datetime import datetime
from math import log
from django.core.files.base import ContentFile

logging.basicConfig(filename='my_log.log', level=logging.DEBUG, encoding='utf-8')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def encode_image_to_base64(image_path):
    logger.info("Начало кодирования картинки в b64")
    try:
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"Файл не найден: {image_path}")
        with open(image_path, 'rb') as image_file:
            
            return base64.b64encode(image_file.read()).decode('utf-8')
        logger.info(f"JPG {image_path}: -> {base64.b64encode()}")
        
    except FileNotFoundError as e:
        logging.error(e)
        return None
    except Exception as e:
        logging.error(f"Произошла ошибка при чтении файла: {e}")
        return None

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# django.setup()

# from models import Event

def update_models():
    pass
#     #Получение сегоднняшней даты (папка в folder)
#     today_date = datetime.date.today().strftime("%Y-%m-%d")
#     frames_folder = os.path.join(settings.MEDIA_ROOT, today_date)

#     if os.path.exists(frames_folder):
#         image_files = [f for f in os.listdis]
    #  object = Event.objects.all()
    #  for obj in object:
    #      obj.description = "123"
    #      obj.save()
    

if __name__ == "__main__":
    update_models()