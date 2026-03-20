from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='case_outcome'),
    
]
