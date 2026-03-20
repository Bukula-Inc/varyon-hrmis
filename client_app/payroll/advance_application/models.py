from client_app.models import BaseModel
from client_app.hr.employee.models import Employee
from client_app.payroll.employee_grade .models import Employee_Grade
from django.db import models
from datetime import date

class Advance_Memo (BaseModel):
    name = models.CharField(max_length=255, unique=True, default='', null=True)
    employee_id = models.ForeignKey (Employee, default=None, null=True, on_delete=models.DO_NOTHING, related_name="advance_memo_employee_id")
    full_name = models.CharField (max_length=255, default="", null= True, blank=True)
    department = models.CharField (max_length=255, default="", null= True, blank=True)
    designation = models.CharField (max_length=255, default="", null= True, blank=True)
    employment_type = models.CharField (max_length=255, default="", null= True, blank=True)
    basic_pay = models.CharField (max_length=255, default="", null= True, blank=True)
    amount_in_words = models.CharField (max_length=255, default="", null= True)
    section = models.CharField (max_length=255, default="", null= True, blank=True)
    amount = models.FloatField (default=0.00, null=True)
    employee_grade = models.ForeignKey (Employee_Grade, on_delete=models.DO_NOTHING, default=None, null=True)
    amount = models.FloatField (default=0.00, null=True)
    advance_type = models.CharField (max_length=255, default="Normal Advance", null=True)
    purpose = models.TextField (blank=True)
    repayment_period = models.IntegerField (default=1, null=True)
    advance_type = models.CharField (max_length=255, default="Normal Advance", null=True)
    cleared = models.IntegerField (default=0, null=True)

    staff_id = models.CharField (max_length=255, default="", null=True)


    class Meta:
        db_table = 'advance_memo'

    def __str__(self) -> str:
        return self.name

class Advance_Application (BaseModel):
    name = models.CharField(max_length=255, unique=True, default='', null=True)
    employee_id = models.ForeignKey (Employee, default=None, null=True, on_delete=models.DO_NOTHING)
    full_name = models.CharField (max_length=255, default="", null= True, blank=True)
    department = models.CharField (max_length=255, default="", null= True, blank=True)
    designation = models.CharField (max_length=255, default="", null= True, blank=True)
    employment_type = models.CharField (max_length=255, default="", null= True, blank=True)
    show_totals = models.CharField (max_length=255, default="", null= True, blank=True)
    emp_status = models.CharField (max_length=255, default="", null= True, blank=True)
    basic_pay = models.CharField (max_length=255, default="", null= True, blank=True)
    amount_in_words = models.CharField (max_length=255, default="", null= True)
    section = models.CharField (max_length=255, default="", null= True, blank=True)
    pay_with_partial_payments = models.IntegerField (default=0, blank=True, null=True)
    amount = models.FloatField (default=0.00, null=True)
    advance_type = models.CharField (max_length=255, default="Normal Advance", null=True)
    amount_with_interest = models.FloatField (default=0.00, null=True)
    purpose = models.TextField (default="", null=True)
    is_paid = models.IntegerField(default=0, null=True)
    is_approved = models.IntegerField(default=0, null=True)
    repayment_period = models.IntegerField(default=0, null=True)
    total_amount_repaid = models.FloatField (default=0.00, null=True)
    total_amount_with_interest_repaid = models.FloatField (default=0.00, null=True)
    total_monthly_amount = models.FloatField (default=0.00, null=True)
    due_date = models.DateField (default=date.today, null=True)
    disbursed_on = models.DateField (default=date.today, null=True)
    employee_grade = models.ForeignKey (Employee_Grade, on_delete=models.DO_NOTHING, default=None, null=True)

    staff_id = models.CharField (max_length=255, default="", null=True)

    class Meta:
        db_table = 'advance_application'

    def __str__(self) -> str:
        return self.name
    

class Second_Salary_Advance_Application (BaseModel):
    name = models.CharField(max_length=255, unique=True, default='', null=True)
    employee_id = models.ForeignKey (Employee, default=None, null=True, on_delete=models.DO_NOTHING)
    full_name = models.CharField (max_length=255, default="", null= True, blank=True)
    department = models.CharField (max_length=255, default="", null= True, blank=True)
    designation = models.CharField (max_length=255, default="", null= True, blank=True)
    employment_type = models.CharField (max_length=255, default="", null= True, blank=True)
    show_totals = models.CharField (max_length=255, default="", null= True, blank=True)
    emp_status = models.CharField (max_length=255, default="", null= True, blank=True)
    basic_pay = models.CharField (max_length=255, default="", null= True, blank=True)
    amount_in_words = models.CharField (max_length=255, default="", null= True)
    section = models.CharField (max_length=255, default="", null= True, blank=True)
    pay_with_partial_payments = models.IntegerField (default=0, blank=True, null=True)
    amount = models.FloatField (default=0.00, null=True)
    advance_type = models.CharField (max_length=255, default="Normal Advance", null=True)
    amount_with_interest = models.FloatField (default=0.00, null=True)
    purpose = models.TextField (default="", null=True)
    is_approved = models.IntegerField(default=0, null=True)
    is_paid = models.IntegerField(default=0, null=True)
    repayment_period = models.IntegerField(default=0, null=True)
    total_amount_repaid = models.FloatField (default=0.00, null=True)
    total_amount_with_interest_repaid = models.FloatField (default=0.00, null=True)
    total_monthly_amount = models.FloatField (default=0.00, null=True)
    due_date = models.DateField (default=date.today, null=True)
    disbursed_on = models.DateField (default=date.today, null=True)
    employee_grade = models.ForeignKey (Employee_Grade, on_delete=models.DO_NOTHING, default=None, null=True)
    second_advance_memo =models.ForeignKey(Advance_Memo, on_delete=models.DO_NOTHING, default=None, null=True)

    staff_id = models.CharField (max_length=255, default="", null=True)

    class Meta:
        db_table = 'second_salary_advance_application'

    def __str__(self) -> str:
        return self.name