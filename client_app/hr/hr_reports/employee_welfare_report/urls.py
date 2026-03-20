from django.urls import path
from .import views
urlpatterns = [
    path('', views.employee_selfare_report, name='employee_selfare_report'),
]