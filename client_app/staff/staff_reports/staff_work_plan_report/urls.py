from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.staff_work_plan_report, name='staff_work_plan_report'),
]