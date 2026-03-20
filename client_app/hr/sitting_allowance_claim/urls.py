from django.urls import path
from . import views

urlpatterns = [
    path ("", views.index, name="sitting_Allowance_claim")
]