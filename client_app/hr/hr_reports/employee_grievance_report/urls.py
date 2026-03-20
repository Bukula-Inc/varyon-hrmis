from django.urls import path
from . import views
urlpatterns = [
    path('', views.employee_grievance_report, name="employee_grievance_report")
]
