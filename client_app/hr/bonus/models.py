from django.db import models
from client_app.hr.employee.models import Employee
from client_app.hr.bonus_types.models import Bonus_Type
from client_app.models import BaseModel, TableModel

class Bonus_To_Employee (TableModel):
    employee = models.ForeignKey (Employee, related_name="bonus_employee", on_delete=models.DO_NOTHING, default=None, null=True)
    employee_name = models.TextField(blank=True, null=True, default="")
    is_scale = models.IntegerField (default=0, null=True)
    is_percentage = models.FloatField (default=0.00, null=True)
    bonus_amount = models.FloatField (default=0.00, null=True)
    basic_pay = models.FloatField (default=0.00, null=True)
    score = models.FloatField (default=0.00, null=True)

    
    def __str__(self) -> str:
        return self.employee.full_name
    
    class Meta:
        db_table = 'bonus_to_employees'

class Bonus(BaseModel):
    name = models.CharField(max_length=255, unique = True, default="")
    bonus_amount = models.FloatField (default=0.00, null=True)
    bonus_type = models.ForeignKey (Bonus_Type, on_delete=models.DO_NOTHING, null=True, default=None, related_name="bonus_type")
    calculation_type = models.CharField (max_length=255, default="", null=True)
    description = models.TextField(blank=True, null=True, default="")
    bonus_employees = models.ManyToManyField (Bonus_To_Employee, blank=True)

    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = 'bonus'