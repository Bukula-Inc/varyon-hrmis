from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="house_loan_agreement")
]
