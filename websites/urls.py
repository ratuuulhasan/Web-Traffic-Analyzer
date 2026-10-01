from django.urls import path
from . import views

app_name = 'websites'

urlpatterns = [
    path('', views.website_list, name='list'),
    path('add/', views.website_add, name='add'),
    path('<int:pk>/', views.website_detail, name='detail'),
    path('<int:pk>/edit/', views.website_edit, name='edit'),
    path('<int:pk>/delete/', views.website_delete, name='delete'),
    path('<int:pk>/export/pageviews.csv', views.export_pageviews_csv, name='export-pageviews'),
    path('<int:pk>/export/visitors.csv', views.export_visitors_csv, name='export-visitors'),
    path('<int:pk>/export/stats.csv', views.export_stats_csv, name='export-stats'),
    path('<int:pk>/email-settings/', views.email_settings, name='email-settings'),
    path('<int:pk>/email-settings/test/', views.send_test_email, name='send-test-email'),
    path('<int:pk>/events/', views.website_events, name='events'),
    path('<int:pk>/map/', views.website_map, name='map'),
]