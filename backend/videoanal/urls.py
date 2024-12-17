from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, consumers

router = DefaultRouter()
router.register(r'event', views.EventViewSet, basename='event')

urlpatterns = [
    path('', include(router.urls)),
    path('upload-video/', views.upload_video, name='upload_video'),
    path('api/events/', views.get_events, name='get_events')
]

websocket_urlpatterns = [
    path('ws/events/', consumers.EventConsumer.as_asgi()),
]