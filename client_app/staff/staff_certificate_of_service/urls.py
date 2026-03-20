from django.urls import path
from . import views

urlpatterns = [
    path ('', views.dashboard, name="staff_certificate_of_service")
]
