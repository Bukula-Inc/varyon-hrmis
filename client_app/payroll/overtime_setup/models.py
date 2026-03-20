from client_app.hr.employee.models import Employee
from client_app.models import BaseModel, TableModel
from client_app.hr.employment_type.models import Employment_Type
from django.db import models

class Overtime_Eligibility (TableModel):
    employment_type = models.ForeignKey (Employment_Type, on_delete=models.DO_NOTHING, default=None, null=True)
    time_measure = models.CharField (max_length=100, blank=True, null=True, default="")
    period_of_service = models.IntegerField (default=0, null=True, blank=True)

    def __str__(self) -> str:
        return self.employment_type.name
    class Meta:
        db_table ='overtime_eligibility'

class Overtime_Configuration(BaseModel):
    name = models.CharField(max_length=255, unique=True, default="", null=True)
    rate_by_working_days = models.FloatField(default=0.00, null=True)
    rate_by_holidays = models.FloatField(default=0.00, null=True)
    calculation_type = models.CharField(max_length=255, default="", null=True)
    number_of_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    salary_type = models.CharField(max_length=255, default="", null=True)
    payment_on_payroll = models.IntegerField(default=0, null=True)
    overtime_type = models.CharField(max_length=255, null=True, default="")
    value_if_fixed = models.FloatField(null=True, default=0.00)
    time_unit = models.CharField(max_length=255, default='', null=True, blank=True)
    fixed_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    eligibility = models.ManyToManyField(Overtime_Eligibility, blank=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta: 
        db_table = 'overtime_configuration'
