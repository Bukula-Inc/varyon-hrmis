from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.nhima_report, name='nhima_report'),
]