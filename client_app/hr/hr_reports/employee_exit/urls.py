from django.urls import path
from . import views

urlpatterns = [
    path ("", views.employee_exit, name="employee_exit"),
]