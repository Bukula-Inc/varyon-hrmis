from django.urls import path

from . import views

urlpatterns = [
    path('', views.training_program_application, name='training_program_application'),
]    