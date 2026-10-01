from django.urls import path
from . import views

urlpatterns = [
    path('track/', views.track_view, name='track'),
    path('track/event/', views.track_event_view, name='track-event'),
    path('stats/', views.stats_api, name='stats'),
    path('realtime/', views.realtime_api, name='realtime'),
    path('realtime/<int:pk>/', views.realtime_website_api, name='realtime-website'),
    path('website/<int:pk>/stats/', views.website_stats_api, name='website-stats'),
    path('website/<int:pk>/events/', views.website_events_api, name='website-events'),
    path('website/<int:pk>/events/list/', views.website_events_list_api, name='website-events-list'),
]