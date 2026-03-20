from django.urls import path
from . import views

urlpatterns = [
    path ("", views.employee_resignation, name="employee_resignation")
]
