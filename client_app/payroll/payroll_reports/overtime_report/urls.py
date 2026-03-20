from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.overtime_report, name='overtime_report'),
]