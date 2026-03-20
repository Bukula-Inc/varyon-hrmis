from django.db import models


from client_app.hr.employee.models import Employee
from client_app.core.company.models import Company
from client_app.core.department.models import Department
from client_app.hr.designation.models import Designation
from client_app.models import BaseModel , TableModel
from datetime import date

class Interviewers(TableModel):
    interviewer= models.CharField(unique=True, null=True)
 
    def __str__(self):
        return f" {self.interviewer}"
    class Meta:
        db_table = 'Interviewers'
class Exit_Questionnair(TableModel):
    question = models.TextField(null=True, default="")
    choice = models.IntegerField(null=True, default=0)
    def __str__(self):
        return self.question
    class Meta:
        db_table = 'exit_questionnair'

class Exit_Interview(BaseModel):
    name = models.CharField(unique=True, max_length=255, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, )
    employee_name =models.CharField(default="", null=True, max_length=255)
    date_of_joining = models.DateField(default=date.today , null=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None, null=True, )
    designation = models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None, null=True, )
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, default=None, null=True, )
    interview_summary =models.TextField(default="", null=True,)
    questions = models.ManyToManyField(Exit_Questionnair, blank=True, default=None)
    interviewers= models.ManyToManyField(Interviewers, blank=True)
    staff_id = models.CharField(max_length=255, default="", null=True)


    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'exit_interview' 



