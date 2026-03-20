from django.urls import path
from . import views

urlpatterns = [
    path ('', views.personal_loan_agreement, name="personal_loan_agreement")
]
