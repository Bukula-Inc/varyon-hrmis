from django.db import models
from datetime import date
from client_app.hr.employee.models import Employee
from client_app.models import BaseModel

# Create your models here.
class Tuition_Advance_For_Salary_Form(BaseModel):
    name = models.CharField(max_length=255, unique=True, default="")
    employee  = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    employee_full_names = models.CharField(max_length=255, null=True, default="")
    email = models.CharField(max_length=255, null=True, default="")
    contact_no = models.CharField(max_length=255, null=True, default="")
    salary_scale = models.CharField(max_length=255, null=True, default="")
    maximum_loan_amount_requested = models.FloatField(default=0.00, null=True)
    maximum_loan_amount_approved = models.FloatField(default=0.00, null=True)
    designation = models.CharField(max_length=255, default="", null=True)
    section = models.CharField(max_length=255, default="", null=True)
    department = models.CharField(max_length=255, default="", null=True)
    repayment_period = models.CharField(max_length=255, default="", null=True)
    monthly_deduction_amount = models.FloatField(default=0.00, null=True)
    nrc_id = models.CharField(max_length=255, null=True, default="")
    date = models.DateField(max_length=255, default=date.today)
    total_amount_repaid = models.FloatField (default=0.00, null=True)
    staff_id = models.CharField(max_length=255, default="", null=True)


    class Meta:
        db_table = "tuition_advance_of_salary_form"

    def __str__(self):
        return self.name