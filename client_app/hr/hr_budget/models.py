from datetime import date
from django.db import models
from client_app.hr.budget_line.models import Budget_Line
from client_app.models import BaseModel, TableModel

# Create your models here.

class HR_Budget_Lines(TableModel):
    budget_line = models.ForeignKey(Budget_Line, on_delete=models.DO_NOTHING, default=None, null=True)
    budget_line_expense = models.FloatField(null=True, default=0.00)
    class Meta:
        db_table="hr_budget_lines"
        
class HR_Budget(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    from_date = models.DateField(null=True, default=date.today)
    to_date = models.DateField(null=True, default=date.today)
    total_funds = models.FloatField(null=True, default=0.00)
    impact_on_budget = models.FloatField(null=True, default=0.00)
    difference = models.FloatField(null=True, default=0.00)
    budget_lines = models.ManyToManyField(HR_Budget_Lines, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table="hr_budget"
        
class HR_Budget_Entries(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    reference_doc = models.CharField(null=True, default="")
    budget_reference = models.CharField(max_length=255, null=True, default="")
    total_allocated = models.FloatField(null=True, default=0.00)
    total_balance = models.FloatField(null=True, default=0.00)
    total_used_amount = models.FloatField(null=True, default=0.00)
    budget_line = models.CharField(max_length=255, null=True, default="")
    entry_type = models.CharField(max_length=255, null=True, default="")

    def __str__(self):
        return self.name
    class Meta:
        db_table = "hr_budget_entries"
    
