from django.db import models


from client_app.models import BaseModel, TableModel
from client_app.core.department.models import Department
from client_app.hr.designation.models import Designation
from client_app.hr.employee.models import Employee
from datetime import date


class Seperation(TableModel):
    activity_name = models.CharField(max_length=255,null=True,default="")
    user = models.ForeignKey( Employee, related_name="users", on_delete=models.DO_NOTHING, default=None,null=True)
    email = models.CharField(max_length=255,null=True, default="")
    begin_on = models.DateField(default=date.today, null=True)
    duration = models.CharField(max_length=255,null=True,default="")
    done = models.IntegerField (default=0, null=True)

    def __str__(self):
        return f" {self.activity_name}"
    class Meta:
        db_table = 'seperation'




class Employee_Seperation(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    employee_name = models.CharField(max_length=255, default='', null=True)
    employee = models.ForeignKey(Employee, related_name="employee", on_delete=models.DO_NOTHING, default=None)
    separation_type = models.CharField(max_length=255, default="", null=True)
    department = models.ForeignKey( Department, on_delete=models.DO_NOTHING, default=None)
    designation = models.ForeignKey( Designation, on_delete=models.DO_NOTHING, default=None)
    resignation_date = models.DateField(default=date.today, null=True)
    reports_to = models.CharField(max_length=255,default="",null=True)
    notice_period = models.CharField(max_length=255,default="",null=True)
    notify_users = models.CharField(max_length=255,default="",null=True)
    reason = models.TextField(max_length=255, null=True,default="")
    last_day_of_work = models.DateField(default=date.today, null=True)
    activities = models.ManyToManyField(Seperation, blank=True)
    skip_exit_interview = models.IntegerField (default=0, null=True)
    skip_final_statement = models.IntegerField (default=0, null=True)
    attachment = models.TextField (blank=True, null=True, default="")

    # NEW FIELDS
    retirement_type =models.CharField(max_length=255,default="",null=True)    
    staff_id = models.CharField(max_length=255, default="", null=True)


    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'employee_seperation'


