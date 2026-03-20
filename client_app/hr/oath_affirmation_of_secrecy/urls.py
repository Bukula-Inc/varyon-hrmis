from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='oath_affirmation_of_secrecy'),
    
]
