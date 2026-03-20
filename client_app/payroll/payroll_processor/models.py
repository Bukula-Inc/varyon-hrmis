from django.db import models
from django.contrib.postgres.fields import JSONField
from client_app.core.company.models import Company
from client_app.core.currency.models import Currency
from client_app.hr.employee.models import Employee
from client_app.models import BaseModel
from datetime import date

def default_employee_info():
    return []

class Payroll_Processor(BaseModel):
    name = models.CharField(unique=True)
    from_date = models.DateField(default=date.today)
    to_date = models.DateField(default=date.today)
    frequency = models.CharField(default="", null=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, default=None,related_name="ppcompany")
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, null=True, default=None,related_name="ppcurrency")
    convertion_rate = models.FloatField(default=1.0, null=True)
    total_employees = models.FloatField(default=1.0, null=True)
    total_failed_payslips = models.IntegerField(default=0, null=True)
    total_successful_payslips = models.IntegerField(default=0, null=True)
    total_basic = models.FloatField(default=0.0, null=True)
    total_gross = models.FloatField(default=0.0, null=True)
    total_net = models.FloatField(default=0.0, null=True)
    total_earnings = models.FloatField(default=0.0, null=True)
    is_previous = models.CharField (max_length=1, null=True, blank=True, default='0')
    is_pp = models.IntegerField(default=0.0, null=True)
    total_deductions = models.FloatField(default=0.0, null=True)
    employee_info = models.JSONField(default=default_employee_info, null=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'payroll_processor'

class Payroll_Activity_Entry (BaseModel):
    name = models.CharField (max_length=255, unique=True)
    employee = models.ForeignKey (Employee, on_delete=models.DO_NOTHING,default=None, null=True)
    amount = models.FloatField (default=0.00, null=True)
    remaining_balance = models.FloatField (default=0.00, null=True)
    monthly_payment = models.FloatField (default=0.00, null=True)
    length_or_period = models.IntegerField (default=0, null=True)
    effective_date = models.DateField (default=date.today, null=True)
    last_payment_date = models.DateField (default=date.today, null=True)
    allows_cash_repayment = models.IntegerField (default=1, null=True)
    month = models.CharField (max_length=255, null=True, default="")
    reference_type = models.CharField (max_length=255, null=True, default="")
    reference = models.CharField (max_length=255, default="", null=True)
    balance = models.FloatField (default=0.00, null=True)
    remaining_period = models.IntegerField (default=0, null=True)
    salary_component = models.CharField (max_length=255, null=True, default="")
    cleared = models.IntegerField (default=0, null=True)
    entry_type = models.CharField (default="Deduction", null=True, max_length=255)
    posting_date = models.DateField (default=date.today, null=True)
    staff_id = models.CharField (max_length=255, default="", null=True)
    salary_advance_type = models.CharField (max_length=255, null=True, default="")
    is_second = models.IntegerField (default=0, null=True)

    class Meta:
        db_table = 'payroll_activity_entries'