from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.dashboard, name='private_insurance_report'),
]