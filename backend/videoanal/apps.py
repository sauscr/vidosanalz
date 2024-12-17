from django.apps import AppConfig

class VideoanalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'videoanal'

    def ready(self):
        import videoanal.signals  # Подключение сигналов
