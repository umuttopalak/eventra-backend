from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from location.models import Location

User = get_user_model()

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)  # Location ile doğru ilişki
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    max_participants = models.IntegerField()
    participants = models.ManyToManyField(User, related_name='attending_events', blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def has_ended(self):
        return timezone.now() > self.end_time
