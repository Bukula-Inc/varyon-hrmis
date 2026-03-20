
from django.contrib import admin
from django.urls import path
from .views import dynamic_page_render, unauthorized

urlpatterns = [
    path ('', unauthorized, name="unauthorized")
    # path('', dynamic_page_render, name='dynamic_page_render'),
    # path('web/<slug:page>/', dynamic_page_render, name='dynamic_page_render'),
    # re_path(r'^(?P<page>.*)/$', dynamic_page_render, name='dynamic_page_render'),
]
