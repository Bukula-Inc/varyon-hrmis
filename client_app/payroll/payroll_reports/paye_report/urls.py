from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.paye_report, name='paye_report'),
]