from datetime import date
from django.db import models
from client_app.core.company.models import Company
from client_app.hr.employee.models import Employee
from client_app.hr.employee_welfare_feedback.models import Employee_Welfare_Survey
from client_app.models import BaseModel, TableModel

# Create your models here.
class Staff_Answer(TableModel):
    question = models.CharField(max_length=255, null=True, default="")
    yes = models.IntegerField(null=True, default=0)
    no  =models.IntegerField(null=True, default=0)
    class Meta:
        db_table ="staff_answer"
class Staff_Welfare_Questionnair(TableModel):
    question = models.CharField(max_length=255, null=True, default="")
    answer = models.CharField(null=True, default="")
    class Meta:
        db_table ="staff_welfare_questionnair"
class Staff_Feedback(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    employee_name = models.CharField(max_length=255, null=True, default="")
    employee_email = models.CharField(max_length=255, null=True, default="")
    name = models.CharField(max_length=255, null=True, default="")
    survey_date = models.DateField(null=True, default=date.today)
    survey = models.ForeignKey(Employee_Welfare_Survey, on_delete=models.DO_NOTHING, null=True, default=None)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, default=None, null=True)
    question_ans = models.ManyToManyField(Staff_Answer, default=None, blank=True)
    staff_welfare_questionnair = models.ManyToManyField(Staff_Welfare_Questionnair, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = "staff_feedback"
    
    