from django.db import models

from client_app.core.company.models import Company
from client_app.core.department.models import Department
from client_app.hr.employee.models import Employee
from client_app.hr.leave_type.models import Leave_Type
from client_app.hr.leave_policy.models import Leave_Policy
from client_app.models import BaseModel, TableModel
from client_app.hr.employee.models import Employee
from client_app.core.company.models import Company
from datetime import date

class Leaves (TableModel):
    leave_type = models.ForeignKey(Leave_Type, on_delete=models.DO_NOTHING, default=None, null=True)
    total_days_allocated_per_month = models.FloatField(null=True, default=0)
    overrall_total = models.FloatField(null=True, default=0)
    apply_on = models.CharField (max_length=255, default='', null=True)

    def __str__(self):
        return f" {self.leave_type}"
    class Meta:
        db_table = 'leaves'

class leave_Allocation_Employees (TableModel):
    employee_name = models.CharField(max_length=255, null=True,default="")
    from_date = models.DateField(default=date.today,null=True)
    to_date = models.DateField(default=date.today,null=True)
    total_leaves_allocated = models.CharField(max_length=255, default="",null=True)
    gender = models.CharField (max_length=10, default="", null=True)
    overall_total_leaves = models.CharField(max_length=255, default="",null=True)
    department = models.ForeignKey(Department,on_delete=models.DO_NOTHING, default=None,null=True)
    employee = models.ForeignKey(Employee, related_name="Leave_allocation_employee", on_delete=models.DO_NOTHING, default=None,null=True)
    leave_policy = models.ForeignKey(Leave_Policy,on_delete=models.DO_NOTHING, default=None,null=True)
    leave_type = models.ForeignKey(Leave_Type,on_delete=models.DO_NOTHING, default=None,null=True)
    def __str__(self):
        return f"{self.leave_type}"
    class Meta:
        db_table = 'leave_allocation_employee'

class Leave_Allocation(BaseModel):
    name = models.CharField(unique=True, null=True, max_length=255)
    company =  models.ForeignKey(Company,on_delete=models.DO_NOTHING, default=None,null=True)
    populate_by = models.CharField (max_length=100, null=True, default="")
    policy = models.CharField (max_length=100, null=True, default="")
    main_policy = models.CharField (max_length=100, null=True, default="")
    main_leave_type = models.CharField (max_length=100, null=True, default="")
    leave_allocation_employees = models.ManyToManyField (leave_Allocation_Employees, related_name="la_by_policy", blank=True)

    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'leave_allocation'