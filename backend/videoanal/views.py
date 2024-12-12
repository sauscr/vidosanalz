from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Event
from .serializers import EventSerializer
from rest_framework.filters import OrderingFilter
from rest_framework import permissions

class EventViewSet(ReadOnlyModelViewSet):
    queryset = Event.objects.all().order_by('-timestamp')
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]  # В будущем заменить на аутентификацию
    filter_backends = [OrderingFilter]
    ordering_fields = ['timestamp']
