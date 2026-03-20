from django.db import models
from client_app.models import BaseModel
from client_app.hr.employee.models import Employee

class Payroll_Arrears (BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    employee = models.ForeignKey( Employee, on_delete=models.DO_NOTHING, default=None, null=True,)
    employee_names = models.CharField(max_length=255, null=True, default="")
    staff_id = models.CharField (max_length=255, default="", null=True)
    arrears = models.JSONField (default=list, null=True)
    
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'payroll_arrears'