from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'), 
    path('accounts/register/', views.register, name='register'),
    path('closet/add/', views.upload_clothing, name='upload_clothing'),
]