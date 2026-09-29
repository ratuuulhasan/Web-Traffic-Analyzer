from django.urls import path
from . import views

urlpatterns = [
    path('track/', views.track_view, name='track'),
    path('stats/', views.stats_api, name='stats'),
]