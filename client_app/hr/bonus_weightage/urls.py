from django.urls import path
from.import views
urlpatterns = [
    path ("", views.bonus_weightage, name = "bonus_weightage")
]