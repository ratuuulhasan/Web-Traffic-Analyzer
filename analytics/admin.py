from django.contrib import admin
from .models import Visitor, PageView


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('visitor_id', 'website', 'country', 'browser', 'os', 'last_visit')
    list_filter = ('browser', 'os', 'country')


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('website', 'url', 'visitor', 'timestamp')
    list_filter = ('website',)