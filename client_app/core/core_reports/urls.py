from django.urls import path, include
# from . import views

urlpatterns = [
    path ("auth_trail/", include ("client_app.core.core_reports.auth_trail.urls")),
    path ("audit_trail/", include ("client_app.core.core_reports.audit_trail.urls")),
]