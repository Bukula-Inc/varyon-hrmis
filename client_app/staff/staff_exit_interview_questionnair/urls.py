from django.urls import path

from . import views

urlpatterns = [
    path ('', views.staff_exit_interview_questionnair, name="staff_exit_interview_questionnair")
]
