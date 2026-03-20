from django.urls import path, include

urlpatterns = [
    path ("items/", include ("client_app.stock.items.urls")),
]