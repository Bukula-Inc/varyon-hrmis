from django.db import models
from client_app.models import BaseModel
from client_app.core.company.models import Company
from client_app.models import BaseModel, TableModel
from client_app.core.company.models import Company
from client_app.hr.employee.models import Employee
from client_app.hr.hr_budget.models import Budget_Line
from client_app.hr.training_program_type.models import Training_Program_Type
from datetime import date


class Attendee(TableModel):
    employee = models.ForeignKey( Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    email =models.CharField(max_length=255, null=True, default="")
    phone_no = models.CharField(max_length=255, null=True, default="")
    class Meta:
        db_table = 'attendee'

class Program_Expense(TableModel):
    expense_type = models.CharField(max_length=255, null=True, default="")
    budget_line = models.ForeignKey (Budget_Line, on_delete=models.DO_NOTHING, default=None, null=True)
    amount = models.FloatField (default=0.00, null=True)
    class Meta:
        db_table = 'program_expense'

class Training_Program(BaseModel):
    name = models.CharField(unique=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, default=None, null=True)
    type = models.ForeignKey(Training_Program_Type, on_delete=models.DO_NOTHING, default=None, null=True)
    course = models.CharField (max_length=255,default="",null=True)
    location = models.CharField (max_length=255,default="",null=True)
    time_date = models.CharField (max_length=255,default="",null=True)
    start_time = models.CharField (max_length=255,default="",null=True)
    end_time = models.CharField (max_length=255,default="",null=True)
    start_date = models.DateField (default=date.today , null=True)
    end_date = models.DateField (default=date.today , null=True)
    program_duration =models.CharField(max_length=255, default=0, null=True)
    trainer= models.CharField(max_length=255,default="",null=True)
    trainer_email = models.TextField(max_length=255,default="",null=True)
    contact = models.CharField(max_length=255,default="",null=True)
    description= models.TextField(default="",null=True)
    reason = models.TextField(default="",null=True)
    training_expense = models.FloatField (default=0.00, null=True)
    attendee = models.ManyToManyField(Attendee, blank=True)
    initiator = models.CharField (max_length=255, default="", null=True)
    expenses = models.ManyToManyField(Program_Expense, blank=True)
    includes_certification = models.IntegerField(default=0, null=True)
    certification_type = models.CharField(max_length=255, null=True, default="")
    other_certificate_type =models.CharField(max_length=255, default="", null=True)
    current_state =models.CharField(max_length=255, default="", null=True)
    training_application_attachment =models.TextField(default="", null=True)

    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'training_program'