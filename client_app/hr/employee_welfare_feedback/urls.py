from django.urls import path
from . import views

urlpatterns = [
    path('',views.employee_welfare_feedback, name="employee_welfare_feedback")
]
