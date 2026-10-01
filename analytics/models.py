from django.db import models
from websites.models import Website


class Visitor(models.Model):
    visitor_id = models.CharField(max_length=64, db_index=True)
    website = models.ForeignKey(
        Website,
        on_delete=models.CASCADE,
        related_name='visitors'
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    browser = models.CharField(max_length=50, blank=True)
    os = models.CharField(max_length=50, blank=True)
    device = models.CharField(max_length=50, blank=True)
    first_visit = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('visitor_id', 'website')

    def __str__(self):
        return self.visitor_id


class PageView(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='pageviews')
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='pageviews')
    url = models.URLField(max_length=500)
    page_title = models.CharField(max_length=255, blank=True)
    referrer = models.URLField(max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.url} - {self.timestamp}"

class Event(models.Model):
    website = models.ForeignKey(
        Website,
        on_delete=models.CASCADE,
        related_name='events'
    )
    visitor = models.ForeignKey(
        Visitor,
        on_delete=models.CASCADE,
        related_name='events',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100, db_index=True)
    properties = models.JSONField(default=dict, blank=True)
    url = models.URLField(max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['website', 'name']),
            models.Index(fields=['website', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.name} - {self.website.name}"