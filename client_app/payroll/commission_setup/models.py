from django.db import models
from client_app.hr.employee.models import Employee
from client_app.models import BaseModel, TableModel

class Commission_Employees(TableModel):
    employee = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    commission_structure = models.CharField(max_length=255, default="", null=True)
    employee_name = models.CharField(max_length=255, default="", null=True)
    user = models.CharField(max_length=255, default="", null=True)
    def __str__(self) -> str:
        return self.employee
    class Meta:
        db_table ='commission_employees'

class Commission_Configuration(TableModel):
    commission_structure = models.CharField(max_length=255, default="", null=True)
    commission_rate = models.CharField(max_length=255, default="", null=True)
    performance_metrics = models.CharField(max_length=255, default="", null=True)
    payment_frequency = models.CharField(max_length=255, default='', blank=True, null=True)
    minimum_payment_threshold = models.CharField(max_length=255, default='', blank=True, null=True)
    commission_rate_type = models.CharField(max_length=255, default='', blank=True, null=True)
    def __str__(self) -> str:
        return self.commission_structure.name
    class Meta:
        db_table ='commission_configuration'

    
class Commission_Setup(BaseModel):
    name = models.CharField(max_length=255, unique=True, default="", null=True)
    configuration = models.ManyToManyField(Commission_Configuration, blank=True)
    employees = models.ManyToManyField(Commission_Employees, blank=True)
    
    def __str__(self) -> str:
        return self.name
    class Meta:
        db_table ='commission_setup'
