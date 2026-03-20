from django.urls import path
from . import views

urlpatterns = [
    path ("", views.index, name="staff_authority_to_council_car")
]