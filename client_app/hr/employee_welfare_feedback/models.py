from datetime import date
from django.db import models
from client_app.core.company.models import Company
from client_app.hr.employee.models import Employee
from client_app.models import BaseModel, TableModel

# Create your models here.
class Employee_Welfare_Questions(TableModel):
    question = models.CharField(max_length=255, null=True, default="")
    total_yes = models.IntegerField(null=True, default=0)
    total_no = models.IntegerField(null=True, default=0)
    yes = models.IntegerField(null=True, default=0)
    no = models.IntegerField(null=True, default=0)
    class Meta:
        db_table="employee_welfare_questions"
class Employee_Welfare_Questionnair(TableModel):
    question = models.CharField(max_length=255, null=True, default="")
    answer = models.IntegerField(null=True, default="")
    class Meta:
        db_table="employee_welfare_questionnair" 
class Employee_Welfare_Survey(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    survey_date = models.DateField(null=True, default=date.today)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, default=None)
    welfare = models.CharField(null=True, default="")
    survey_welfare = models.CharField(null=True, default="")
    other_survey_welfare = models.CharField(null=True, default="")
    welfare_questions = models.ManyToManyField(Employee_Welfare_Questions, blank=True)
    employee_welfare_questionnair = models.ManyToManyField(Employee_Welfare_Questionnair,blank=True)
    staff_id = models.CharField(max_length=255, default="", null=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table="employee_welfare_survey"