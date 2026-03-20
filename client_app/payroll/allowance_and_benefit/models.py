from django.db import models

# Create your models here.
from client_app.models import BaseModel, TableModel
from client_app.payroll.employee_grade.models import Employee_Grade

class Allowance_and_Benefit_Category(TableModel):
    salary_grade =models.ForeignKey(Employee_Grade, on_delete=models.DO_NOTHING, default=None, null=True)
    amount =models.FloatField(default=0.00, null=True)
    transportation =models.CharField(max_length=255, default="", null=True)
    in_patient =models.FloatField(default=0.00, null=True)
    out_patient =models.FloatField(default=0.00, null=True)
    optical =models.FloatField(default=0.00, null=True)
    dental =models.FloatField(default=0.00, null=True)

    class Meta:
        db_table ="allowance_and_benefit_category"

class Allowance_and_Benefit(BaseModel):
    name =models.CharField(max_length=255, default="", null=True)
    description =models.TextField(default="", null=True)
    categories =models.ManyToManyField(Allowance_and_Benefit_Category, blank=True)
    extra_fields =models.CharField(max_length=255, default="", null=True)
    affects_payroll =models.IntegerField(default=0, null=True)
    create_salary_component =models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table ="allowance_and_benefit"