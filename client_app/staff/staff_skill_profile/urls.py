from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff_skill_profile, name="staff_skill_profile")
]
