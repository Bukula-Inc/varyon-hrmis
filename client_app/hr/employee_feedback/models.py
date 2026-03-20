from django.db import models


from client_app.hr.employee.models import Employee
from client_app.models import BaseModel
from client_app.core.department.models import Department




class Employee_Feedback(BaseModel):
    name = models.CharField(unique=True,max_length=255, null=True)
    questions= models.CharField(max_length=255,default="",null=True)
    comments= models.CharField(max_length=255,default="",null=True)
    your_feedback= models.CharField(max_length=255,default="",null=True)
    email= models.CharField(max_length=255,default="",null=True)
    first_name= models.CharField(max_length=255,default="",null=True)
    last_name= models.CharField(max_length=255,default="",null=True)
    staff_id = models.CharField(max_length=255, default="", null=True)

    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'employee_feedback'


