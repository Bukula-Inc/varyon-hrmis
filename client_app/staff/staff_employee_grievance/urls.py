from django.urls import path
from . import views

urlpatterns = [
    path ("", views.staff_employee_grievance, name="staff_employee_grievance")
]