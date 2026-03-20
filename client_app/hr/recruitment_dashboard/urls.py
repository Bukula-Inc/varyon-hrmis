from django.urls import path
from . import views 

urlpatterns = [
    path ("", view=views.dashboard, name="recruitment_dashboard")
]