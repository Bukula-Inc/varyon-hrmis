from django.urls import path
from . import views

urlpatterns = [
    path ('', views.dashboard, name="graduate_development_enrollment")
]
