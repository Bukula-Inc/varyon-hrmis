from django.db import models
from django.utils import timezone
from client_app.core.company.models import Company
from client_app.core.department.models import Department
from client_app.hr.designation.models import Designation
from client_app.hr.employee.models import Employee
from client_app.hr.leave_type.models import Leave_Type
from client_app.models import BaseModel

from datetime import date

class Employee_Attendance (BaseModel):
    name = models.CharField(unique=True, max_length=255,null=True, default="")
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name="attendance_employee")
    employee_name = models.CharField(max_length=255,default="",null=True)
    attendance_date = models.DateField(default=date.today,null=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, default=None, null=True, related_name="attendance_company")
    department =models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None, null=True, related_name="attendance_dept")
    shift = models.CharField(max_length=255,default="",null=True, choices=[
        ("Morning", "Morning"), 
        ("Afternoon", "Afternoon"),
        ("Evening", "Evening"),
        ("Night", "Night"),
        ("Day", "Day"),
    ])
    
    total_hours_worked = models.DecimalField(max_digits=4, decimal_places=2, null=True, default=0, blank=True)
    leave_type = models.ForeignKey(Leave_Type, on_delete=models.DO_NOTHING, null=True, default=None,)
    designation = models.ForeignKey (Designation, on_delete=models.DO_NOTHING, null=True,default=None, related_name='attendance_designation')
    manager = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=True, default=None, related_name='attendance_manager')
    time_in = models.DateTimeField(default=timezone.now, null=True, blank=True, editable=False)
    time_out = models.DateTimeField(default=timezone.now, null=True, blank=True)
    staff_id = models.CharField(max_length=255, default="", null=True)


    def __str__(self):
        return f'{self.employee_name}'

    class Meta:
        db_table = 'employee_attendance'