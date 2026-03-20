from django.db import models

from client_app.hr.employee.models import Employee

from client_app.models import BaseModel
from datetime import date
from django.utils import timezone



class Employee_Checkin(BaseModel):
    name = models.CharField(unique=True, max_length=255,null=True)
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    employee_name = models.CharField(max_length=255, default="",null=True)
    checkin_time= models.CharField(default="",null=True)
    log_type = models.CharField(max_length=255, default="", null=True)
    device    = models.CharField(max_length=255, default="", null=True)
    staff_id = models.CharField(max_length=255, default="", null=True)

    
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'employee_checkin' 



