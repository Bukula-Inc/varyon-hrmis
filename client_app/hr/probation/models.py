from django.db import models
from client_app.hr.employee.models import Employee
from client_app.models import BaseModel, TableModel
from controllers.utils import Utils
from controllers.utils.dates import Dates
from datetime import date

utils =Utils


# Create your models here.
class Probation(BaseModel):
    name =models.CharField(unique=True, max_length=255, default="", null=True)
    probation_length =models.IntegerField(default=0, null=True)
    basic_pay =models.FloatField(default=0, null=True)
    # length_intervals =models.CharField(max_length=255, default="", null=True)

    deductions = models.JSONField(default=list, null=True)
    earnings = models.JSONField(default=list, null=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'probation'

    
class Probation_List(BaseModel):
    name =models.CharField(unique=True, max_length=255, default="", null=True)
    employee =models.CharField(max_length=255, default="", null=True)
    start_date =models.DateField(default=date.today, null=True)
    due_date =models.DateField(default=date.today, null=True)
    probation_length =models.IntegerField(default=0, null=True)
    probation_status =models.IntegerField(default=0, null=True)
    staff_id = models.CharField(max_length=255, default="", null=True)


    def __str__(self):
        return self.name
    class Meta:
        db_table = 'probation_list'