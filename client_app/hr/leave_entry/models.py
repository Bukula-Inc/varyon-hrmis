from django.db import models


from client_app.hr.leave_type.models import Leave_Type
from client_app.hr.leave_policy.models import Leave_Policy
from client_app.hr.employee.models import Employee
from client_app.hr.leave_allocation.models import Leave_Allocation
from client_app.hr.leave_application.models import Leave_Application
from client_app.models import BaseModel
from datetime import date




class Leave_Entry(BaseModel):
    name = models.CharField(unique=True, null=True)
    reference =models.ForeignKey(Leave_Allocation, on_delete=models.DO_NOTHING, default=None, null=True)
    cancel_reference = models.ForeignKey (Leave_Application, on_delete=models.DO_NOTHING, null=True, default=None)
    total_days = models.FloatField(null=True,default=0,blank=True)
    leave_type = models.ForeignKey(Leave_Type,on_delete=models.DO_NOTHING, default=None,null=True)
    employee = models.ForeignKey(Employee,on_delete=models.DO_NOTHING,max_length=255,default=None,null=True)
    employee_name = models.CharField(max_length=255,default="",null=True)
    from_date = models.DateField(default=date.today,null=True)
    to_date = models.DateField(default=date.today,null=True)
    used_leave_days = models.FloatField(blank=True, null=True,default=0)
    allocated_leave_days = models.FloatField(blank=True, null=True,default=0)
    remaining_leave_days = models.FloatField(blank=True, null=True,default=0)
    leave_days_in_working_hours = models.CharField (max_length=255, null=True, default=None)
    is_active = models.IntegerField (default=0, null=True)
    entry_type = models.CharField (max_length=255, default="", null=True)
    staff_id = models.ForeignKey(Employee,on_delete=models.DO_NOTHING,max_length=255,default=None,null=True, related_name="leave_entry_staff_id")


    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'leave_entry'

class Leave_Mapper (BaseModel):
    name = models.CharField (max_length=255, unique=True, default='', null=True)
    employee = models.ForeignKey (Employee, related_name="leave_mapper_employee", on_delete=models.DO_NOTHING, default=None, null=True)
    leave_policy = models.ForeignKey (Leave_Policy, related_name="leave_mapper_leave_policy", on_delete=models.DO_NOTHING, default=None, null=True)
    leave_type = models.ForeignKey (Leave_Type, related_name="leave_mapper_leav_ty", on_delete=models.DO_NOTHING, default=None, null=True)
    staff_id = models.CharField(max_length=255, default="", null=True)



    def __str__(self):
        return self.name
    class Meta:
        db_table = 'leave_mapper'
