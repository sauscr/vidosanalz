from django.db import models

class Event(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='frames/%d-%m-%Y/')
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Event at {self.timestamp}"
