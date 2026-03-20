from django.urls import path
from . import views

urlpatterns = [
    path ("", views.resgnation, name="witness")
]
