from django.urls import path
from. import views

urlpatterns = [
    path('', views.staff_interview_evaluator, name="staff_interview_evaluator")
]
