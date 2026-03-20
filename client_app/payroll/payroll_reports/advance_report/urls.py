from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.advance_report, name='advance_report'),
]