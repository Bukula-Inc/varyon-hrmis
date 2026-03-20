from django.db import models

# Create your models here.

from client_app.hr.leave_type.models import Leave_Type
from client_app.hr.employee.models import Employee
from client_app.core.department.models import Department
from client_app.models import BaseModel
from datetime import date




class Leave_Compensation(BaseModel):
    name = models.CharField(null=True, unique=True)
    employee = models.ForeignKey(Employee,on_delete=models.DO_NOTHING, default=None,null=True)
    employee_name = models.CharField(max_length=255,default="",null=True)
    leave_type = models.ForeignKey(Leave_Type,on_delete=models.DO_NOTHING, default=None,null=True)
    department = models.ForeignKey(Department,on_delete=models.DO_NOTHING, default=None,null=True)
    from_date = models.DateField(default=date.today)
    to_date = models.DateField(default=date.today)
    half_day = models.CharField(max_length=255,null=True)
    reason = models.CharField(max_length=255,default="",null=True)
    staff_id = models.CharField(max_length=255, default="", null=True)


    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'leave_compensation'


