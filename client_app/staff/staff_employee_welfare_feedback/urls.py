from django.urls import path
from . import views

urlpatterns = [
    path ('', views.staff_employee_welfare_feedback, name="staff_employee_welfare_feedback")
]
