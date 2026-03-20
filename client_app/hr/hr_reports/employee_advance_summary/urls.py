from django.urls import path
from . import views

urlpatterns = [
    path ("", views.employee_advance_summary, name="employee_advance_summary"),
]