from django.contrib import admin
from .models import Website


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'owner', 'tracking_id', 'created_at')
    search_fields = ('name', 'domain')
    readonly_fields = ('tracking_id',)