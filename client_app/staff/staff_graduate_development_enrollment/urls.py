from django.urls import path
from . import views

urlpatterns = [
    path ('', views.dashboard, name="staff_graduate_development_enrollment/")
]
