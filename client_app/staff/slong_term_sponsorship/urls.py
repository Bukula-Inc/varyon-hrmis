from django.urls import path
from . import views
urlpatterns = [
    path ("", views.dashboard, name="long_term_sponsorship"),
]