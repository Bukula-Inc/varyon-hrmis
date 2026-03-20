from django.db import models
from client_app.hr.employee.models import Employee
from client_app.core.company.models import Company
from client_app.core.department.models import Department
from client_app.hr.designation.models import Designation
from client_app.payroll.salary_component.models import Salary_Component
from client_app.models import BaseModel , TableModel
from datetime import date
# Create your models here.



class Calculated_Totals(TableModel):
    salary = models.CharField(max_length=255, default="", null=True, )
    leave_days_amount = models.CharField(max_length=255, default="", null=True, )
    overtime_amount =models.CharField(max_length=255, default="", null=True, )
    unsettled_loan =models.CharField(max_length=255, default="", null=True, )
    redundancy_amount =models.CharField(max_length=255, default="", null=True, )
    gratuity_amount =models.CharField(max_length=255, default="", null=True, )

    class Meta:
        db_table = 'calculated_totals'
class Statement_Asset(TableModel):
    # assets_reference_document = models.ForeignKey(Asset, on_delete=models.DO_NOTHING, default=None, null=True, )
    assets_reference_document = models.CharField(default="", null=True, max_length=255)
    assets_reference_document_type = models.CharField(max_length=255, default="", null=True, )
    assets_component =models.CharField(default="", null=True, max_length=255)
    assets_amount =models.IntegerField(default=0, null=True, )
    assets_status =models.CharField(default="", max_length=255, null=True, )

    class Meta:
        db_table = 'statement_asset'

class Payable(TableModel):
    component = models.ForeignKey(Salary_Component, on_delete=models.DO_NOTHING, default=None, null=True, )
    reference_document_type = models.CharField(max_length=255, default="", null=True, )
    reference_document =models.CharField(default="", null=True, max_length=255)
    amount =models.IntegerField(default=0, null=True, )
    payable_status =models.CharField(default="", null=True, max_length=255)
   
    class Meta:
        db_table = 'payable'

class Receivable (TableModel):
    component = models.ForeignKey(Salary_Component, on_delete=models.DO_NOTHING, default=None, null=True, )
    reference_document_type = models.CharField(max_length=255, default="", null=True, )
    reference_document = models.CharField(default="", null=True, max_length=255)
    amount =models.IntegerField(default=0, null=True, )
    payable_status =models.CharField(default="", null=True, max_length=255)
   
    class Meta:
        db_table = 'receivables'

class Final_Statement(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    statement_for = models.CharField (max_length=2355, null=True, default='')
    employee_name = models.CharField(max_length=255, default='', null=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, )
    date_of_joining = models.DateField(default=date.today )
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None, null=True, )
    designation = models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None, null=True, )
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, default=None, null=True, )
    transaction_date = models.DateField(default=date.today , null=True)
    total_payable =models.IntegerField(default=0, null=True, )
    total_asset =models.IntegerField(default=0, null=True, )
    leave_days = models.FloatField(default=0.00, null=True, )
    redundancy = models.FloatField(default=0.00, null=True, )
    gratuity = models.FloatField(default=0.00, null=True, )
    payable = models.ManyToManyField(Payable, related_name='related_payables', blank=True)
    receivables = models.ManyToManyField(Receivable, related_name='related_receivables', blank=True)
    calculated_totals = models.ManyToManyField(Calculated_Totals, related_name='calculated_totals', blank=True)
    asset = models.ManyToManyField(Statement_Asset, related_name='statement_asset', blank=True)
   
    
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'final_statement' 



