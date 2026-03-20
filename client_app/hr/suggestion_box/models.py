from django.db import models

from client_app.hr.employee.models import Employee
from client_app.core.department.models import Department
from client_app.hr.suggestion_category.models import Suggestion_Category

from client_app.models import BaseModel
from datetime import date



class Suggestion_Box(BaseModel):
    name = models.CharField(unique=True, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    employee_name = models.CharField(max_length=255, default="",null=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None, null=True)
    posting_date = models.DateField(default=date.today,null=True)
    category = models.ForeignKey(Suggestion_Category, on_delete=models.DO_NOTHING, default=None, null=True)
    suggestion_context = models.TextField(max_length=255,  default="",null=True)
    yes= models.CharField(max_length=255, default="",null=True)
    no = models.CharField(max_length=255, default="",null=True)
    staff_id = models.CharField(max_length=255, default="", null=True)


    def __str__(self):
        return self.name
    class Meta:
        db_table = 'suggestion_box'



