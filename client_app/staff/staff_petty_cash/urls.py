from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.dashboard, name='staff_petty_cash/'),
]