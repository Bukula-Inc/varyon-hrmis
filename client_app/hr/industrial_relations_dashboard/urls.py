from django.urls import path
from . import views 

urlpatterns = [
    path ("", view=views.dashboard, name="industrial_relations_dashboard")
]