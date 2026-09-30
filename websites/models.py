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

class EmailReportSetting(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    website = models.OneToOneField(
        Website,
        on_delete=models.CASCADE,
        related_name='email_report'
    )
    is_enabled = models.BooleanField(default=False)
    frequency = models.CharField(
        max_length=10,
        choices=FREQUENCY_CHOICES,
        default='daily'
    )
    send_hour = models.PositiveIntegerField(
        default=9,
        help_text='Hour of day (0-23) to send email'
    )
    last_sent = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.website.name} - {self.frequency} report"