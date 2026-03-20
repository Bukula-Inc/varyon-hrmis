from django.urls import path
from . import views

urlpatterns = [
    path ("", views.self_appraisal_report, name="self_appraisal_report"),
]