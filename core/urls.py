from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'), 
    path('accounts/register/', views.register, name='register'),
    path('closet/add/', views.upload_clothing, name='upload_clothing'),
    path('closet/roll/', views.roll_wardrobe, name='roll_wardrobe'),
    path('closet/toggle/<str:day_name>/', views.toggle_day_confirmation, name='toggle_day_confirmation'),
]