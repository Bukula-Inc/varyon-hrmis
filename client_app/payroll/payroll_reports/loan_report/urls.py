from django.urls import path
from . import views

urlpatterns = [
    path ("", views.appraisal_report, name="loan_report"),
]