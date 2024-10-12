# models.py
from dj_rest_kit.models import BaseUUIDModel
from django.db import models
from django.conf import settings


class Message(BaseUUIDModel):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']