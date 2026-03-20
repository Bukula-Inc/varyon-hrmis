from django.urls import path
from . import views

urlpatterns = [
    path ("", views.employee_leave_balance, name="employee_leave_balance"),
]