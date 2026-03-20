from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.skills_levy_report, name='skills_levy_report'),
]