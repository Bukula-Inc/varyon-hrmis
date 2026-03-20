from django.urls import path
from . import views

urlpatterns = [
    path ('', views.training_program_report, name="training_program_report")
]
