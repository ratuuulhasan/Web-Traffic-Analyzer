from django.urls import path
from . import views

urlpatterns = [
    path('track/', views.track_view, name='track'),
    path('stats/', views.stats_api, name='stats'),
    path('realtime/', views.realtime_api, name='realtime'),
    path('realtime/<int:pk>/', views.realtime_website_api, name='realtime-website'),
    path('website/<int:pk>/stats/', views.website_stats_api, name='website-stats'),
]