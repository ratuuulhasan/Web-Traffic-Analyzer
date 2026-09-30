from django.urls import path
from . import views

app_name = 'api_v1'

urlpatterns = [
    path('websites/', views.WebsiteListView.as_view(), name='websites'),
    path('websites/<int:pk>/', views.WebsiteDetailView.as_view(), name='website-detail'),
    path('websites/<int:pk>/stats/', views.WebsiteStatsView.as_view(), name='website-stats'),
    path('websites/<int:pk>/pageviews/', views.PageViewListView.as_view(), name='pageviews'),
    path('websites/<int:pk>/visitors/', views.VisitorListView.as_view(), name='visitors'),
    path('websites/<int:pk>/realtime/', views.RealtimeView.as_view(), name='realtime'),
    path('websites/<int:pk>/countries/', views.CountryBreakdownView.as_view(), name='countries'),
]