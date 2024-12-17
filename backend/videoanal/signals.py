from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Event)
def update_event(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'events', {
                'type': 'new_event',
                'event': {
                    'id': instance.id,
                    'timestamp': instance.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'image': instance.image.url,
                    'description': instance.description,
                }
            }
        )