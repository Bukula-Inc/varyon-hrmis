from django.urls import path
from . import views

urlpatterns = [
    path ('', views.skills_inventory, name="skills_inventory_dashboard")
]
