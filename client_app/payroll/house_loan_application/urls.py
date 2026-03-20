from django.urls import path
from . import views

urlpatterns = [
    path('', views.house_loan_application, name="house_loan_application")
]
