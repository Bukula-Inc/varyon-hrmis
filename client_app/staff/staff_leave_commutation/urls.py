from django.urls import path
from .import views

urlpatterns = [
    path ('', views.staff_leave_commutation, name="staff_leave_commutation")
]
