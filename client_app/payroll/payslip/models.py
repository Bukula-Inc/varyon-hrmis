from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
from datetime import date
from client_app.hr.employee.models import Employee
from client_app.payroll.employee_grade.models import Employee_Grade
from client_app.core.department.models import Department
from client_app.hr.designation.models import Designation
from client_app.hr.employment_type.models import Employment_Type
from client_app.payroll.income_tax_band.models import Income_Tax_Band
from client_app.payroll.salary_component.models import Salary_Component
from client_app.payroll.payroll_processor.models import Payroll_Processor
from client_app.models import BaseModel, TableModel
from client_app.core.currency.models import Currency
from client_app.core.company.models import Company
# Create your models here.

def default_component():
    return {}

class Payslip_Earning(TableModel):
    earning = models.ForeignKey(Salary_Component, on_delete=models.DO_NOTHING, default=None, null=True, related_name="ps_earming")
    amount = models.FloatField(null=True)
    units = models.IntegerField (null=True, default=1)
    class Meta:
        db_table = 'payslip_earning'

class Payslip_Deduction(TableModel):
    deduction = models.ForeignKey(Salary_Component, on_delete=models.DO_NOTHING, default=None, null=True, related_name="ps_deduction")
    amount = models.FloatField(null=True)
    outstanding = models.IntegerField(null=True)
    balance = models.FloatField(null=True)
    units = models.CharField (max_length=255, default="", null=True)
    class Meta:
        db_table = 'payslip_deduction'

class Payslip(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    posting_date = models.DateField(default=date.today,)
    from_date = models.DateField(default=date.today,)
    to_date = models.DateField(default=date.today,)
    posting_time = models.DateTimeField(default=timezone.now,)
    reporting_currency = models.ForeignKey( Currency, on_delete=models.DO_NOTHING, default=None, null=True, related_name="ps_reporting_currency")
    currency = models.ForeignKey( Currency, on_delete=models.DO_NOTHING, default=None, null=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, default=None, null=True)
    convertion_rate = models.FloatField(null=True, default=0)
    employee = models.ForeignKey( Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name="psemp")
    employee_names = models.CharField(max_length=255, null=True, default="")
    department = models.ForeignKey( Department, on_delete=models.DO_NOTHING, default=None, null=True, related_name="psdept")
    designation = models.ForeignKey( Designation, on_delete=models.DO_NOTHING, default=None, null=True, related_name="psdesg")
    employment_type = models.ForeignKey( Employment_Type, on_delete=models.DO_NOTHING, default=None, null=True, related_name="psemptype")
    payroll_frequency = models.CharField(max_length=255, null=True)
    working_days = models.IntegerField(null=True,default=26)
    current_leave_days = models.IntegerField(null=True,default="")
    current_leave_value = models.FloatField(null=True, default=0.00)
    basic_pay = models.FloatField(null=True, default=0.00)
    gross = models.FloatField(null=True, default=0.00)
    total_earnings = models.FloatField(null=True, default=0.00)
    total_tax_amount = models.FloatField(null=True, default=0.00)
    total_deductions = models.FloatField(null=True, default=0.00)
    advance_amount = models.FloatField(null=True, default=0.00, blank=True)
    advance_repaid = models.FloatField(null=True, default=0.00, blank=True)
    pension_paid = models.FloatField(null=True, default=0.00, blank=True)
    total_advance_repaid = models.FloatField(null=True, default=0.00, blank=True)
    net = models.FloatField(null=True, default=0.00)
    payroll_processor = models.ForeignKey( Payroll_Processor, on_delete=models.DO_NOTHING, default=None, null=True, related_name="ppss")
    earnings = models.JSONField(default=default_component, null=True)
    deductions = models.JSONField(default=default_component, null=True)
    bank_name = models.CharField(max_length=255, null=True, default="")
    pay_point = models.CharField(max_length=255, null=True, default="")
    bank_account_no = models.CharField(max_length=255, null=True,default="")
    tax_identification_no = models.CharField(max_length=255, null=True,default="")
    ssn = models.CharField(max_length=255, null=True,default="")
    salary_grade = models.ForeignKey (Employee_Grade, on_delete=models.DO_NOTHING, default=None, null=True)
    tax_band  = models.ForeignKey( Income_Tax_Band, on_delete=models.DO_NOTHING, default=None, null=True, related_name="tbnd")
    ytd_gross = models.FloatField(null=True, default=0.00)
    ytd_net = models.FloatField(null=True, default=0.00)
    ytd_earnings = models.FloatField(null=True, default=0.00)
    ytd_deductions = models.FloatField(null=True, default=0.00)
    napsa = models.FloatField(null=True, default=0.00)
    ytd_napsa = models.FloatField(null=True, default=0.00)
    ytd_pla = models.FloatField(null=True, default=0.00)
    ytd_tax = models.FloatField(null=True, default=0.00)
    ytd_leave_days = models.FloatField(null=True, default=0.00)
    ytd_leave_value = models.FloatField(null=True, default=0.00)
    years_in_service = models.CharField(max_length=255, null=True,default="")
    private_pension = models.FloatField(null=True, default=0.00)
    ytd_private_pension = models.FloatField(null=True, default=0.00)
    incremental = models.FloatField(null=True, default=0.00)
    staff_id = models.CharField (max_length=255, default="", null=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'payslip'

class Advance_And_Pension_Entries (BaseModel):
    name = models.CharField(max_length=255, unique=True)
    employee = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, null=True, default=None)
    posting_date = models.DateField (default=date.today, null=True)
    ref_doc = models.CharField (max_length=255, default="", null=True)
    ref = models.CharField (max_length=255, null=True, default="")
    salary_component = models.CharField (max_length=255, null=True, default="")
    amount_saved = models.FloatField (default=0.00, null=True)
    is_recovered = models.IntegerField (default=0, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'advance_and_pension_entries'