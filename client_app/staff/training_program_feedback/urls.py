from django.urls import path

from . import views

urlpatterns = [
    path ("", views.training_program_feedback, name="training_program_feedback")
]
