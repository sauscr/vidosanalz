from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Event
from .serializers import EventSerializer
from .tasks import analyze_frame_task
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .tests import encode_image_to_base64, update_models
import os
import logging

# Настройка логирования
logging.basicConfig(filename='my_log.log', level=logging.DEBUG, encoding='utf-8')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]  # В будущем заменить на аутентификацию
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['timestamp']
    
@csrf_exempt
def upload_video(request):
    if request.method == 'POST':
        logger.info("Начало загрузки видео")
        video_file = request.FILES['video']
        save_path = os.path.join(settings.MEDIA_ROOT, 'videos', video_file.name)
        path = default_storage.save(save_path, video_file)
        logger.info(f"Видео сохранено по пути: {save_path}")
        os.system(f'python manage.py capture_stream --url "{save_path}" --source_type "file" --interval 1')
        logger.info("Анализ видео начат")
        return JsonResponse({'message': 'Видео успешно загружено и анализ начат'}, status=200)
    logger.warning("Получен не POST запрос")
    return JsonResponse({'error': 'Только POST запросы принимаются'}, status=400)

@api_view(['GET'])
def get_events(request):
    update_models()
    logger.info("Получение списка событий")
    events = Event.objects.all().order_by('-timestamp')  # Получаем все события, отсортированные по времени
    serializer = []
    for event in events:

        event_data = EventSerializer(event).data
        # image_base64 = encode_image_to_base64(event.image.path)
        # event_data['image_base64'] = image_base64
        serializer.append(event_data)
    logger.info(f"Отправлено {len(serializer)} событий")
    return JsonResponse(serializer, safe=False)
    # def get(self, request):
    #     data = cache.get('event')
    #     if not data:
    #         queryset = Event.objects.all().order_by('-timestamp')
    #         for backend in list(self.filter_backends):
    #             queryset = backend().filter_queryset(request, queryset, self)
    #         serializer = EventSerializer(queryset, many=True)
    #         data = serializer.data
    #         cache.set('event', data)
    #     return Response(data)
