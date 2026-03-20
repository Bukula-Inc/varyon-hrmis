from django.urls import path 
from . import views

urlpatterns = [
    path ('', views.employee_seperation_dashboard, name="employee_separation_dashboard")
]
