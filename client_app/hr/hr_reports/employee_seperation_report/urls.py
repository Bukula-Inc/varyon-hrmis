from django.urls import path
from . import views
urlpatterns = [
    path('', views.employee_seperation_report, name='employee_seperation_report'),
]