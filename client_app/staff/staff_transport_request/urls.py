from django.urls import path
from . import views

urlpatterns = [
    path('', views.transport_request, name="staff_transport_request")
]
