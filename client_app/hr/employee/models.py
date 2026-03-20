from django.db import models
from datetime import date
from client_app.core.company.models import Company
from client_app.core.currency.models import Currency
from client_app.core.department.models import Department
from client_app.hr.designation.models import Designation
from client_app.payroll.income_tax_band.models import Income_Tax_Band
from client_app.hr.employment_type.models import Employment_Type
from client_app.payroll.employee_grade.models import Employee_Grade
from client_app.core.branch.models import Branch
from client_app.authentication.models import Lite_User
from client_app.hr.section.models import Section


from client_app.core.branch.models import Branch
from client_app.models import BaseModel

class Employee(BaseModel):
    name = models.CharField(max_length=255, default="",null=True, unique=True, blank=True)
    first_name = models.CharField(max_length=255, default="",null=True, blank=True)
    middle_name = models.CharField(max_length=255, default="",null=True, blank=True)
    last_name = models.CharField(max_length=255, default="",null=True, blank=True)
    full_name = models.CharField(max_length=255, default="",null=True, blank=True)
    gender = models.CharField(max_length=255, default="",null=True, blank=True)
    d_o_b = models.DateField(default=date.today, null=True, blank=True)

    salutation = models.CharField(max_length=255, default="",null=True, blank=True)
    id_no = models.CharField(max_length=255, default="",null=True, blank=True)
    nhima = models.CharField(max_length=255, default="",null=True, blank=True)
    napsa = models.CharField(max_length=255, default="",null=True, blank=True)
    tpin = models.CharField(max_length=255, default="",null=True, blank=True)
    employment_type =models.ForeignKey(Employment_Type, on_delete=models.DO_NOTHING, default=None, null=True, blank=True)
    company =models.ForeignKey(Company, on_delete=models.DO_NOTHING, default=None, null=True, blank=True)
    date_of_joining = models.DateField(default=date.today, null=True, blank=True)
    last_day_of_work = models.DateField(default=date.today, null=True, blank=True)
    create_user = models.CharField(max_length=255, default="",null=True, blank=True)
    user = models.ForeignKey(Lite_User, on_delete=models.DO_NOTHING, default=None, null=True, blank=True)
    email = models.CharField(max_length=255, default="",null=True, blank=True)
    contact = models.CharField(default=0,null=True, blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None, null=True, blank=True)
    branch =  models.ForeignKey(Branch, on_delete=models.DO_NOTHING, default=None, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None, null=True, blank=True)
    inable_probation = models.IntegerField(null=True,default=0, blank=True)
    probation = models.CharField(max_length=255, default="", null=True, blank=True)
    employee_saved = models.IntegerField (default=0, null=1, blank=True)
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING, default=None, null=True, blank=True)
    report_to = models.CharField(max_length=255, default=None,null=True, blank=True)
    leave_approver = models.CharField(max_length=255, default=None,null=True, blank=True)
    shift_approver = models.CharField(max_length=255, default=None,null=True, blank=True)
    requisition = models.CharField(max_length=255, default=None,null=True, blank=True)
    basic_pay = models.FloatField(default=0.00, null=True, blank=True)
    bank_branch = models.CharField(max_length=255, null=True,default="", blank=True)
    bank_name = models.CharField(max_length=255, null=True,default="", blank=True)
    account_no= models.CharField(max_length=255, null=True,default="", blank=True)
    sort_code= models.CharField(max_length=255, null=True,default="", blank=True)
    employee_grade = models.ForeignKey(Employee_Grade, on_delete=models.DO_NOTHING, default=None, null=True, blank=True)
    tax_band = models.ForeignKey(Income_Tax_Band, on_delete=models.DO_NOTHING, default=None, null=True, blank=True)
    working_days = models.IntegerField(null=True,default=0, blank=True)
    working_hours = models.IntegerField(null=True,default=0, blank=True)
    currency = models.ForeignKey (Currency, on_delete=models.DO_NOTHING, default=None, null=True, blank=True)
    
    is_separated = models.IntegerField (default=0, null=True, blank=True)
    is_separated_emp_paid = models.CharField (max_length=50, default="Unsettled", null=True, blank=True)

    deductions = models.JSONField(default=list, null=True, blank=True)
    earnings = models.JSONField(default=list, null=True, blank=True)
    unstandardized_components = models.JSONField(default=list, null=True)
    end_of_contract =models.DateField(default=date.today, null=True, blank=True)
    contract = models.CharField(default=0,null=True, blank=True)


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'employee'


class Enabled_Bonding_Period (BaseModel):
    name = models.CharField (max_length=255, unique=True)
    employee = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    enabled_on = models.DateField (default=date.today , null=True)
    ending_on = models.DateField (default=date.today , null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'bonding_period_tb'
class Employee_Pay_And_Salary (BaseModel):
    name = models.CharField (max_length=255, unique=True)
    employee = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    basic_pay = models.FloatField (default=0.00, null=True)
    tax_band = models.ForeignKey(Income_Tax_Band, on_delete=models.DO_NOTHING, default=None, null=True)
    employee_grade = models.ForeignKey(Employee_Grade, on_delete=models.DO_NOTHING, default=None, null=True)
    earnings = models.JSONField (default=list, null=True)
    deductions = models.JSONField (default=list, null=True)
    is_current = models.IntegerField (default=0, null=True)
    promoted = models.IntegerField (default=0, null=True)
    date_of_promotion = models.DateField (default=date.today, null=True)
    previous_salary = models.JSONField (default=list, null=True)
    working_days = models.IntegerField(null=True,default=0)
    working_hours = models.IntegerField(null=True,default=0)
    currency = models.ForeignKey (Currency, on_delete=models.DO_NOTHING, default=None, null=True)
    employment_status = models.CharField (max_length=50, null=True, default="")


    def __str__(self):
        return self.name
    class Meta:
        db_table = 'employee_salary'
