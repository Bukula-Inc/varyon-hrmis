from django.urls import path

from . import views

urlpatterns = [
    path ("", views.staff_performance_agreement, name="staff_performance_agreement")
]
