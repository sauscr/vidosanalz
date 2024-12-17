from rest_framework import serializers
from .models import Event
from urllib.parse import quote

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'timestamp', 'image', 'description']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            image_url = request.build_absolute_uri(obj.image.url)
            return quote(image_url, safe=':/')
        return None