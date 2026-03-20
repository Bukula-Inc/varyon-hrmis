from django.urls import path
from . import views

urlpatterns = [
    path('', views.budget_line, name="budget_line")
]
