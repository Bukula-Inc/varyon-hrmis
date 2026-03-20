from django.urls import path
from . import views

urlpatterns = [
    path ("", views.monthly_attendance, name="monthly_attendance"),
]