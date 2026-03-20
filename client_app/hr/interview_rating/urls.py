from django.urls import path

from . import views

urlpatterns = [
    path('', views.interview_rating, name="interview_rating")
]
