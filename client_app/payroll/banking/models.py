from client_app.models import BaseModel
from client_app.hr.employee.models import Employee
from client_app.payroll.employee_grade .models import Employee_Grade
from django.db import models
from datetime import date

class Bank_Account (BaseModel):
    name = models.CharField (max_length=255, null=True, unique=True)
    account_code = models.CharField (max_length=255, null=True, default="")
    descriptions = models.CharField (max_length=255, null=True, default="")
    is_credit = models.IntegerField (default=0, null=True)
    is_debit = models.IntegerField (default=0, null=True)

    class Meta:
        db_table = "bank_account"

class Bank (BaseModel):
    name = models.CharField (max_length=255, null=True, unique=True)
    descriptions = models.CharField (max_length=255, null=True, default="")

    class Meta:
        db_table = "bank"

class Account_Branch_Code (BaseModel):
    name = models.CharField (max_length=255, null=True, unique=True)
    descriptions = models.CharField (max_length=255, null=True, default="")
    bank = models.ForeignKey (Bank, on_delete=models.DO_NOTHING, null=True, default=None)
    sort_code = models.CharField (max_length=250, default="", null=True)
    class Meta:
        db_table = "account_branch_code"
