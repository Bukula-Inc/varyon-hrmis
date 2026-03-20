from django.db import models

# Create your models here.
from django.db import models
from client_app.core.company.models import Company
from client_app.models import BaseModel, TableModel
from datetime import date

class Taxable_Salary_Band(TableModel):
    amount_from = models.CharField(max_length=255, default='', null=True)
    amount_to = models.CharField(max_length=255, default='', null=True)
    deduction_percentage = models.FloatField(default=0.00, null=True)
    class Meta:
        db_table = 'taxable_salary_band'


class Income_Tax_Band(BaseModel):
    name = models.CharField(unique=True)
    effective_from = models.DateField(default=date.today, null=True)
    is_current = models.CharField(max_length=255, default="1", null=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, default=None)
    deduct_on = models.CharField(max_length=255, null=True, default="")
    zra_percentage = models.FloatField(default=0, null=True)
    take_home_percentage = models.FloatField(default=0, null=True)
    tax_free_amount = models.FloatField(default=0, null=True)
    salary_bands = models.ManyToManyField(Taxable_Salary_Band, related_name="salary_bands", blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'income_tax_band'