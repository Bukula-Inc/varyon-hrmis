from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.dashboard, name='staff_leave_plan'),
]