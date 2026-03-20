from django.db import models
from client_app.hr.employee.models import Employee
from client_app.models import BaseModel, TableModel
from datetime import date

class Overtime_Worked (TableModel):
    day = models.CharField (max_length=50, default="", null=True)
    date_of_work = models.DateField (default=date.today, null=True)
    from_time = models.CharField (max_length=20, default="", null=True)
    to_time = models.CharField (max_length=20, default="", null=True)
    total_hours = models.CharField (max_length=20, default="", null=True)
    rate = models.FloatField (default=0.00, null=True)
    total_amount = models.FloatField (default=0.00, null=True)
    emp_basic = models.FloatField (default=0.00, null=True)
    emp_wrk_hrs = models.IntegerField (default=0, null=True)
    emp_wrk_days = models.IntegerField (default=0, null=True)
    cleared = models.IntegerField (default=0, null=True)

    def __str__(self):
        return f" {self.day}"
    class Meta:
        db_table = 'overtime_worked_list'


class Overtime_CLaim (BaseModel):
    name = models.CharField (max_length=255, unique=True)
    employee = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    fullname = models.CharField (max_length=255, default="", null=True)
    salary_grade = models.CharField (max_length=255, default="", null=True)
    designation = models.CharField (max_length=255, default="", null=True)
    department = models.CharField (max_length=255, default="", null=True)
    month = models.CharField (max_length=255, default="", null=True)
    show = models.CharField (max_length=255, default="", null=True)
    attachment = models.TextField (blank=True, null=True, default="")
    purpose = models.TextField (blank=True, null=True, default="")
    overtime_worked = models.JSONField (default=list, null=True)
    hours_worked =models.FloatField(default=0.00, null=True)
    # overtime_worked = models.ManyToManyField (Overtime_Worked, blank=True, default=None,)
    staff_id = models.CharField (max_length=255, default="", null=True)

    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'overtime_claim'