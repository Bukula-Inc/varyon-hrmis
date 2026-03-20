from django.db import models


from client_app.models import BaseModel, TableModel
from client_app.core.company.models import Company
from client_app.hr.training_program.models import Training_Program
from client_app.hr.employee.models import Employee


class Employees_Training(TableModel):
    employee = models.ForeignKey( Employee, on_delete=models.DO_NOTHING,null=True, default=None)
    email =models.CharField(max_length=255, null=True, default="")
    employee_status = models.CharField(max_length=255)
    employee_attendance = models.CharField(max_length=255)
    mandatory = models.CharField(max_length=255)

    def __str__(self):
        return f" {self.employee}"
    class Meta:
        db_table = 'employees_training'




class Training_Event(BaseModel):
    name = models.CharField(unique=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, default=None, null=True)
    type = models.TextField(max_length=255,default="",null=True)
    level= models.TextField(max_length=255,default="",null=True)
    has_certificate = models.CharField(max_length=255,null=True)
    trainer= models.CharField(max_length=255,default="",null=True)
    trainer_email = models.TextField(max_length=255,default="",null=True)
    contact = models.CharField(max_length=255,default="",null=True)
    course = models.CharField(max_length=255,default="",null=True)
    location= models.CharField(max_length=255,default="",null=True)
    start_date = models.CharField(max_length=255,default="",null=True)
    end_date = models.CharField(max_length=255,default="",null=True)
    start_time = models.TextField(max_length=255,default="",null=True)
    end_time = models.CharField(max_length=255,default="",null=True)
    introduction= models.TextField(max_length=255,default="",null=True)
    employees = models.ManyToManyField(Employees_Training, blank=True)

    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'training_event'


