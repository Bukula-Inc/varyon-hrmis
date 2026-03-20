from django.contrib import admin
from django.urls import path, include
from services import request_handler

urlpatterns = [
    path('new-tenant/', request_handler.new_tenant),
    path('migrate/', request_handler.migrate),
    path('full-migration/', request_handler.full_migration),
    path('create-default-data/', request_handler.create_tenant_default_data),
    path('delete-module-migrations/', request_handler.delete_module_migrations),
    path('delete-module-tables/', request_handler.delete_module_tables),
]
