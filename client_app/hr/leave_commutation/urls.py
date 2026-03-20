from django.urls import path 
from . import views

urlpatterns = [
    path ('', views.leave_commutation, name="leave_commutation")
]
