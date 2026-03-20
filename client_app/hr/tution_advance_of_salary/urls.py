from django.urls import path
from . import views

urlpatterns = [
    path ('', views.tution_advance_of_salary, name="tution_advance_of_salary")
]
