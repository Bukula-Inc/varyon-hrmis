from django.db import models

# Create your models here.
from django.db import models
from client_app.core.company.models import Company
from client_app.core.currency.models import Currency
from client_app.models import BaseModel, TableModel
from client_app.payroll.salary_component.models import Salary_Component

class Employee_Grade_Earning(TableModel):
    component = models.ForeignKey(Salary_Component, on_delete=models.DO_NOTHING, null=True, default='')
    class Meta:
        db_table = 'employee_grade_earning'

class Employee_Grade_Deduction(TableModel):
    component = models.ForeignKey(Salary_Component, on_delete=models.DO_NOTHING, null=True, default='')
    class Meta:
        db_table = 'employee_grade_deduction'


class Employee_Grade(BaseModel):
    name = models.CharField(unique=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, related_name="g_company",default="")
    payment_frequency = models.CharField(default="Monthly")
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, related_name="g_currency",default="")
    basic_pay = models.FloatField(default=0.00)
    earnings = models.ManyToManyField(Employee_Grade_Earning, related_name="g_earnings", blank=True)
    deductions = models.ManyToManyField(Employee_Grade_Deduction, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'employee_grade'