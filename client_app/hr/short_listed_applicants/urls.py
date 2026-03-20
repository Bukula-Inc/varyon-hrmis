from django.urls import path
from . import views

urlpatterns = [
    path ('', views.short_listed_applicants, name="short_listed_applicants")
]
