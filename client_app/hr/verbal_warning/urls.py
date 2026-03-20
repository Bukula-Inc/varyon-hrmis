from django.urls import path
from . import views

urlpatterns = [
    path ('', views.verbal_warning, name="verbal_warning")
]
