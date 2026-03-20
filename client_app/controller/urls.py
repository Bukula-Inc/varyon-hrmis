from django.urls import path, include

urlpatterns = [
    path ('', include ('client_app.controller.controller_dashboard.urls')),
    path ('controller_dashboard', include ('client_app.controller.controller_dashboard.urls')),
    path ('background_job/', include ('client_app.controller.background_job.urls')),
    path('controller_dashboard/', include('client_app.controller.controller_dashboard.urls')),
    path('billing_config/', include('client_app.controller.billing_config.urls')),
    path('module_group/', include('client_app.controller.module_group.urls')),
    path('module_pricing/', include('client_app.controller.module_pricing.urls')),
    path('tenant/', include('client_app.controller.tenant.urls')),
    path('license/', include('client_app.controller.license.urls')),
    path('subscription/', include('client_app.controller.subscription.urls')),
    path('module/', include('client_app.controller.module.urls')),
    path('domain_controller/', include('client_app.controller.domain_controller.urls')),
    path('user_pool/', include('client_app.controller.user_pool.urls')),
]
