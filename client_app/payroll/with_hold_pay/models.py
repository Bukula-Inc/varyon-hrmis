from django.db import models
from client_app.models import BaseModel
from client_app.hr.employee.models import Employee
from datetime import date

class With_Hold_Employee_Pay (BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    is_current = models.IntegerField (default=0, null=True)
    with_held_for = models.IntegerField (default=0, null=True)
    fully_payed = models.IntegerField (default=0, null=True)
    from_date = models.DateField (default=date.today, null=True)
    to_date = models.DateField (default=date.today, null=True)
    employees = models.JSONField (default=list, null=True)
    staff_id = models.CharField (max_length=255, default="", null=True)
    
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'with_hold_employee_pay'