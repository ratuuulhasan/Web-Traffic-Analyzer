from django.contrib import admin
from .models import Visitor, PageView


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('visitor_id', 'website', 'country', 'browser', 'os', 'device', 'last_visit')
    list_filter = ('country', 'browser', 'os', 'device')
    search_fields = ('visitor_id', 'ip_address', 'country')


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('website', 'url', 'visitor', 'timestamp')
    list_filter = ('website',)