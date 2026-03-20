from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.dashboard, name='employee_on_leave'),
]