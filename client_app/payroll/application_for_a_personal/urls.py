from django.urls import path
from . import views

urlpatterns =[
    path("", views.dashboard, name="application_for_a_personal/")
]
