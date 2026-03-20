from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff_house_loan_application, name="staff_house_loan_application")
]
