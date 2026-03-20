from django.db import models
from client_app.hr.designation.models import Designation
from client_app.hr.employee.models import Employee
from client_app.hr.employee_disciplinary.models import Employee_Disciplinary
from client_app.models import BaseModel
from datetime import date



class Disciplinary_Statement_Form(BaseModel):
    name =models.CharField(unique=True, max_length=255, null=True)

    employee =models.CharField(max_length=255, default="", null=True)
    employee_name =models.CharField(max_length=255, default="", null=True)
    age =models.CharField(max_length=255, default="", null=True)
    nrc =models.CharField(max_length=255, default="", null=True)
    job_title =models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default="", null=True)
    position_in_matter =models.CharField(max_length=255, default="", null=True)
    charge =models.CharField (max_length=255, default="", null=True)

    statament_attachment =models.TextField(default="", null=True)
    statement =models.TextField(default="", null=True)
    date_engaged =models.DateField(default=date.today, null=True)
    staff_id = models.CharField(max_length=255, default="", null=True)


    def __str__(self):
        return self.name
    class Meta:
        db_table = 'disciplinary_statement_form' 
