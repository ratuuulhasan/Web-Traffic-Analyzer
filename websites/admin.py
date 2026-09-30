from django.contrib import admin
from .models import Website, APIKey


class APIKeyInline(admin.StackedInline):
    model = APIKey
    extra = 0
    readonly_fields = ('key', 'created_at', 'last_used')


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'owner', 'tracking_id', 'created_at')
    search_fields = ('name', 'domain')
    readonly_fields = ('tracking_id',)
    inlines = [APIKeyInline]


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('website', 'key', 'is_active', 'created_at', 'last_used')
    list_filter = ('is_active',)
    search_fields = ('key', 'website__name')
    readonly_fields = ('key', 'created_at', 'last_used')