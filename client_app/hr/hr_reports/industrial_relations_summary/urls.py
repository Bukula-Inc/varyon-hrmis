from django.urls import path
from . import views
urlpatterns = [
    path('', views.employee_grievance_report, name="industrial_relations_summary")
]
