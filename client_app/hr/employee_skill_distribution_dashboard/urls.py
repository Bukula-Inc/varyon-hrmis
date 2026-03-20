from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_skill_distribution_dashboard, name="employee_skill_distribution_dashboard")
]
