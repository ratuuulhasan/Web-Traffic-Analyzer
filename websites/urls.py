from django.urls import path
from . import views

app_name = 'websites'

urlpatterns = [
    path('', views.website_list, name='list'),
    path('add/', views.website_add, name='add'),
    path('<int:pk>/', views.website_detail, name='detail'),
    path('<int:pk>/edit/', views.website_edit, name='edit'),
    path('<int:pk>/delete/', views.website_delete, name='delete'),
    
]