from django.db import models
from client_app.core.company.models import Company
from client_app.hr.leave_type.models import Leave_Type
from client_app.core.department.models import Department
from client_app.hr.employee.models import Employee
from client_app.models import BaseModel
from datetime import date

class Leave_Application(BaseModel):
    name = models.CharField(unique=True, null=True)
    employee = models.ForeignKey(Employee,on_delete=models.DO_NOTHING, default=None, null=True)
    employee_name = models.CharField(max_length=255,default="", null=True)
    delegated_officer = models.ForeignKey(Employee, related_name="delegated_officer_la", on_delete=models.DO_NOTHING, default=None, null=True)
    delegated_officer_name = models.CharField(max_length=255,default="", null=True)
    leave_type = models.ForeignKey(Leave_Type,on_delete=models.DO_NOTHING, default=None, null=True)
    company =  models.ForeignKey(Company,on_delete=models.DO_NOTHING, default=None, null=True)
    department = models.ForeignKey(Department,on_delete=models.DO_NOTHING, default=None, null=True)
    from_date = models.DateField(default=date.today,null=True)
    to_date = models.DateField(default=date.today,null=True)
    reason = models.CharField(max_length=255,default="",null=True)
    attachment = models.CharField(max_length=255,default="",null=True)
    total_days = models.FloatField(default=0,null=True)
    leave_approver = models.CharField(max_length=255,default="",null=True)
    leave_approver_name = models.CharField(max_length=255,default="",null=True)
    leave_mode = models.CharField (max_length=50, null=True, default="")
    from_time = models.CharField (max_length=50, default="", null=True)
    to_time = models.CharField (max_length=50, default="", null=True)
    time_duration_formatted = models.CharField (max_length=50, default="", null=True)
    handover_notes = models.TextField (blank=True, default="", null=True)
    staff_id = models.CharField(max_length=255, default="", null=True)
    approved = models.IntegerField (default=0, null=True)

    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'leave_application'