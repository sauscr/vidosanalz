from django.db import models
from pathlib import Path

class Event(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='frames/%d-%m-%Y/')
    # description = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    # identified_employees = models.TextField(blank=True, null=True)  # Список идентифицированных сотрудников

    def __str__(self):
        return f"Event at {self.timestamp}"
  
    def save(self, *args, **kwargs):
        # Преобразование пути к изображению в строку, если это WindowsPath
        if isinstance(self.image, Path):
            self.image = str(self.image)
        super().save(*args, **kwargs)