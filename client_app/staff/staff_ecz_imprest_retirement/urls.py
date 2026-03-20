from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.dashboard, name='staff_ecz_imprest_retirement'),
]