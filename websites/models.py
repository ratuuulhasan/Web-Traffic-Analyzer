import uuid
from django.db import models
from django.contrib.auth.models import User


class Website(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='websites')
    name = models.CharField(max_length=100)
    domain = models.URLField()
    tracking_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.domain})"