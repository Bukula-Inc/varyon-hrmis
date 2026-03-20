from django.urls import path
from . import views
urlpatterns = [
    path ('', views.welfare_type, name="welfare_type")
]
