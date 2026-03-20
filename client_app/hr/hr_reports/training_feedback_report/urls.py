from django.urls import path

from . import views

urlpatterns = [
    path("", views.training_ffedback_report, name="training_feedback_report")
]
