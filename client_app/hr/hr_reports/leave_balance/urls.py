from django.urls import path
from . import views

urlpatterns = [
    path ("", views.leave_balance, name="leave_balance"),
]