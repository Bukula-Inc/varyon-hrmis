from django.urls import path
from . import views

urlpatterns = [
    path ("", views.employee_contacts, name="employee_contacts"),
]