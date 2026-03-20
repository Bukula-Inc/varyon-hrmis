from django.urls import path
from . import views

urlpatterns = [
    path('', views.exit_interview_questionnair, name='exit_interview_questionnair'),
    
]