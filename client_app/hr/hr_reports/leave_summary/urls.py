from django.urls import path 
from . import views

urlpatterns = [
    path ("", views.leave_summary, name="leave_summary")
]
