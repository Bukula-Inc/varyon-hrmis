from django.contrib import admin

from client_app.payroll.employee_grade.models import Employee_Grade, Employee_Grade_Deduction, Employee_Grade_Earning

# Register your models here.
admin.site.register(Employee_Grade_Earning)
admin.site.register(Employee_Grade_Deduction)
admin.site.register(Employee_Grade)