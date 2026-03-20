from django.urls import path
from.import views
urlpatterns = [
    path ("", views.bonus_threshold, name = "bonus_threshold")
]