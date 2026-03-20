from django.db import models
from client_app.hr.employee.models import Department, Employee
from client_app.models import BaseModel
from datetime import date
# Create your models here.

class Verbal_Warning(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    employee_full_name = models.CharField (max_length=255, null=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=True, default=None)
    employee_department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True)
    employee_job_title = models.CharField(null=True, default="")
    advised_action = models.CharField(max_length=255, null=True, default="")
    action_subject = models.CharField(max_length=255, null=True, default="")
    discription_of_violation = models.TextField (blank=True, null=True, default="")
    warning_officer =models.CharField(null=True, default="")
    fullname = models.CharField(max_length=255, null=True, default="")
    position = models.CharField(max_length=255, null=True, default="")
    warning_date = models.DateField(null=True, default=date.today)
    signing_date =models.DateField(default=date.today, null=True)
    date_of_violation =models.DateField(default=date.today, null=True)


    warning_officer_full_name = models.CharField(max_length=255, null=True, default="")
    warning_officer_job_title = models.CharField(max_length=255, null=True, default="")
    staff_id = models.CharField(max_length=255, default="", null=True)

    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'verbal_warning' 