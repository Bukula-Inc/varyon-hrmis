from django.urls import path, include
from . import views

urlpatterns = [
    path('', include ('client_app.onboarding.welcome.urls'), name='onboarding'),
    path ('welcome', include ('client_app.onboarding.welcome.urls')),
]