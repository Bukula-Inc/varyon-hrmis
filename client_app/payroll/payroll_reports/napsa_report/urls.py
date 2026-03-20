from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.napsa_report, name='napsa_report'),
]