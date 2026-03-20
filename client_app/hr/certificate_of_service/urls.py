from django.urls import path
from . import views

urlpatterns = [
    path ('', views.dashboard, name="certificate_of_service")
]
