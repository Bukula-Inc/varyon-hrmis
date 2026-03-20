from django.db import models
from client_app.models import BaseModel, TableModel
from client_app.payroll.advance_application.models import Employee_Grade


class Salary_Increment(BaseModel):
    name =models.CharField(max_length=255, default="", null=True, unique=True)
    increment_type =models.CharField(max_length=255, default="", null=True)
    salary_grades =models.JSONField (default=list, null=True)
    description =models.TextField(default="", null=True)
    employee_updates =models.JSONField (default=list, null=True)
    grade_updates =models.JSONField (default=list, null=True)
    saved = models.IntegerField (default=0, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table ="salary_increment"