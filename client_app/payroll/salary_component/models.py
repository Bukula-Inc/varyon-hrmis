from django.db import models
from client_app.core.company.models import Company
from client_app.models import BaseModel, TableModel

class Salary_Component_Custom_Formula (TableModel):
    component = models.CharField (max_length=100, blank=True, null=True, default="")
    representation = models.CharField (max_length=100, blank=True, null=True, default="")
    def __str__(self) -> str:
        return self.component
    class Meta:
        db_table ='salary_component_custom_formula'

class Salary_Component(BaseModel):
    name = models.CharField(unique=True)
    custom_formula = models.IntegerField(default=0, null=True)
    formula = models.CharField(max_length=255, default="", null=True)
    component_type = models.CharField(default="Earning")
    old_name = models.CharField(max_length=255, null=True, default="")
    percentage = models.FloatField(default=0.00, null=True)
    value_type = models.CharField(default="",blank=True, null=True)
    effective_date = models.CharField(default="",blank=True, null=True)
    shared_deduction_custom_company = models.CharField(default="",blank=True, null=True)
    shared_deduction_custom_emp = models.CharField(default="",blank=True, null=True)
    apply_on = models.CharField(max_length=255,default="",blank=True, null=True)
    fixed_amount = models.FloatField(default=0.00, null=True)
    has_ceiling = models.IntegerField(default=0, null=True)
    ceiling_amount = models.FloatField(default=0.00, null=True)
    shared_deduction = models.IntegerField(default=0, null=True)
    is_standard_component = models.IntegerField(default=0, null=True)
    is_statutory_component = models.IntegerField(default=0, null=True)
    for_commutation = models.IntegerField(default=0,blank=True, null=True)
    is_private_pension = models.IntegerField(default=0, null=True)
    is_overtime = models.IntegerField(default=0, null=True)
    is_advance = models.IntegerField(default=0, null=True)
    account = models.CharField (max_length=255, null=True, default="")
    account_code = models.CharField (max_length=255, null=True, default="")
    is_commission = models.IntegerField(default=0, null=True)
    is_type = models.CharField(max_length=255,default="",blank=True, null=True)
    unstandardized = models.IntegerField(default=0, null=True)
    is_to_catch_up = models.IntegerField(default=0, null=True)
    grossable = models.IntegerField(default=0, null=True)
    shared_deduction_custom = models.IntegerField(default=0, null=True)
    exclude_on_statutory_deductions = models.IntegerField(default=0, null=True)
    custom_formula_section = models.JSONField (default=list, null=True)
    resenting = models.CharField (max_length=255, default="", null=True)
    unites = models.CharField (max_length=255, default="", null=True)
    
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'salary_component'