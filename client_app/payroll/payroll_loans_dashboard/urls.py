from django.urls import path
from . import views

urlpatterns = [
    path ('', views.dashboard, name="payroll_loans_dashboard")
]