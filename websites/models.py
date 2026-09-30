import uuid
from django.db import models
from django.contrib.auth.models import User
import secrets


class Website(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='websites')
    name = models.CharField(max_length=100)
    domain = models.URLField()
    tracking_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.domain})"
class APIKey(models.Model):
    website = models.OneToOneField(Website, on_delete=models.CASCADE, related_name='api_key')
    key = models.CharField(max_length=64, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_key():
        return 'ta_' + secrets.token_urlsafe(40)[:48]

    def __str__(self):
        return f"API Key for {self.website.name}"