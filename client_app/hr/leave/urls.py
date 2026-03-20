from django.urls import path , include
from . import views

urlpatterns = [
    path('leave-type/', include('client_app.hr.leave.leave_type.urls')),
    path('leave/', include('client_app.hr.leave.leave.urls')),
    path('leave-create/', views.leave_create, name='leave-create'),
    path('employee-leave-balance/', views.employee_leave_balance, name='employee-leave-balance'),
    path('leave-allocation/', views.leave_allocation, name='leave-allocation'),
    path('leave-type/', views.leave_type, name='leave-type'),
]
