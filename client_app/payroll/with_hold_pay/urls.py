from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.dashboard, name='with_hold_pay'),
]