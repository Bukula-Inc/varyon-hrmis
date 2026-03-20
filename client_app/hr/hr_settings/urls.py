from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='hr_settings'),
    
]