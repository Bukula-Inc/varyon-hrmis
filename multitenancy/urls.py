from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import  static
from . import settings
from .settings import MEDIA_ROOT, MEDIA_URL

# from debug_toolbar import urls as debug_urls
urlpatterns = [
    path("",include('website.urls')),
    path('api/', include('api.urls')),
    path('services/', include('services.urls')),
    path('app/controller/', include('client_app.controller.urls')),
    path('auth/', include('client_app.authentication.urls')),
    path('app/core/', include('client_app.core.urls')),
    path('app/hr/', include('client_app.hr.urls')),
    path('app/payroll/', include('client_app.payroll.urls')),
    path('app/stock/', include ('client_app.stock.urls')),
    path('app/staff/', include('client_app.staff.urls')),
    path('app/onboarding/', include('client_app.onboarding.urls')),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)