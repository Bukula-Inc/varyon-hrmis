from django.urls import path, include
from . import views

urlpatterns =[
    path("", views.dashboard, name="imprest_a/")
]
