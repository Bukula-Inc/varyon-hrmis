from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='employee'),
    # path('create-employee', views.employee_create, name='create-employee'),
    # path('employee-checkin-create',
    #      views.employee_checkin_create, name='employee-checkin'),
    # path('attendance', views.attendance, name='attendance'),
    # path('checkin', views.checkin, name='checkin'),
    # path('attendance-create', views.attendance_create, name='attendance-create'),
    # path('monthly-attendance-sheet', views.monthly_attendance_sheet,
    #      name='monthly-attendance-sheet'),
    # path('employee-information', views.employee_information,
    #      name='employee-information'),
    # path('salary-advance', views.salary_advance_list, name='salary-advance'),
    # path('salary-advance-create', views.salary_advance_create,
    #      name='salary-advance-create'),
    # path('promotion', views.promotion, name='promotion'),
    # path('employee-promotion-create', views.employee_promotion_create,
    #      name='employee-promotion-create'),
    # path('branch', views.branch, name='branch'),
    # path('branch-create', views.branch_create, name='branch-create'),
    # path('employee-birthday', views.employee_birthday, name='employee-birthday'),
    # path('advance-summary', views.employee_advance_summary, name='advance-summary'),
    # path('employee-exit', views.employee_exit, name='employee-exit'),
    # path('employee-contacts', views.employee_contacts, name='employee-contacts'),
]
