from datetime import date
from django.db import models
from client_app.core.department.models import Department
from client_app.hr.employee.models import Employee
from client_app.hr.employee_separation.models import Employee_Seperation
from client_app.models import BaseModel, TableModel
from client_app.hr.designation.models import Designation

# Create your models here.
class Questions(TableModel):
    question = models.TextField(null=True, default="")
    answer = models.TextField(null=True, default="")
    def __str__(self):
        return self.question
    class Meta:
        db_table ="questions"


class Open_Ended_Exit_Questionnaire(TableModel):
    question =models.CharField(max_length=255, default="", null=True)
    answer =models.TextField(default="", null=True)
    class Meta:
        db_table ="open_ended_exit_questionnaire"

class Closed_Ended_Exit_Questionnaire(TableModel):
    question =models.CharField(max_length=255, default="", null=True)
    answer =models.CharField(max_length=255, default="", null=True)

    class Meta:
        db_table ="closed_ended_exit_questionnaire"
class Exit_Interview_Questionnair(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    designation = models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None, null=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None,null=True)
    due_date = models.DateField(null=True, default=date.today)
    email = models.CharField(max_length=255, null=True, default="")
    last_day = models.DateField(null=True, default=date.today)
    questions = models.ManyToManyField(Questions, blank=True, related_name="exit_questions")
    open_ended_questions =models.ManyToManyField(Open_Ended_Exit_Questionnaire, blank=True, related_name="exit_questionnaire")
    closed_ended_questions =models.ManyToManyField(Closed_Ended_Exit_Questionnaire, blank=True, related_name="exit_questionnaire")
    employee_seperation = models.ForeignKey(Employee_Seperation, on_delete=models.DO_NOTHING, default=None,null=True)
    staff_id = models.CharField(max_length=255, default="", null=True)


    def __str__(self):
        return self.name
    class Meta:
        db_table="exit_interview_questionnair"
