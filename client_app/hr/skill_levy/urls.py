from django.urls import path
from . import views

urlpatterns = [
    path ('', views.skill_levy, name="skill_levy")
]
