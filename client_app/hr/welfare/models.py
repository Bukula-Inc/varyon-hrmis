from django.db import models
from client_app.hr.employee.models import Department, Employee, Employee_Grade
from client_app.models import BaseModel


class Recovery_Of_Medical_Bills (BaseModel):
    name = models.CharField(max_length=255, unique=True)
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=True, default=None)
    salary_scale = models.ForeignKey(Employee_Grade, on_delete=models.DO_NOTHING, null=True, default=None)
    employee_name = models.CharField (max_length=255, null=True)
    section = models.CharField (max_length=255, null=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True)
    designation = models.CharField(null=True, default="")
    amount_in_words = models.CharField(null=True, default="")
    payment_length = models.IntegerField(null=True, default=0)
    company_covered_expense = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True, default=0.00)
    staff_covered_expense = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True, default=0.00)
    welfare_expense = models.FloatField(null=True, default=0.00)
    monthly_repayment_amount = models.FloatField (default=0.00, null=True)
    attach_receipt = models.TextField (blank=True, null=True, default="")
    cleared =models.IntegerField(default=0, null=True)

    payment_method =models.CharField(max_length=255, default="", null=True)
    total_amount_repaid = models.FloatField (default=0.00, null=True)
    staff_id = models.CharField(max_length=255, default="", null=True)


    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'recovery_of_medical_bills' 