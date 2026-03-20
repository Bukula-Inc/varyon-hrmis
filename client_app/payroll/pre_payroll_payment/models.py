from django.db import models
from client_app.hr.employee.models import Employee, Employee_Grade
from client_app.models import  BaseModel, TableModel
from client_app.payroll.allowance_and_benefit.models import Allowance_and_Benefit

def default_child_table():
    return list

class Pre_Payroll_payment(BaseModel):
    name =models.CharField(max_length=255, unique=True, default="", null=True)

    Total_amount =models.FloatField(default=0.00, null=True)
    total_basic =models.FloatField(default=0.00, null=True)
    total_gross =models.FloatField(default=0.00, null=True)
    total_deduction =models.FloatField(default=0.00, null=True)
    total_net =models.FloatField(default=0.00, null=True)

    separations =models.JSONField(default=default_child_table(), null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table ="pre_payroll_payment"