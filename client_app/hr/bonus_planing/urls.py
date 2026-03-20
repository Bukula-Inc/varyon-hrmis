from django.urls import path
from.import views
urlpatterns = [
    path ("", views.bonus_planing, name = "bonus_planing")
]