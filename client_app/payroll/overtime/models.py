from django.db import models
from client_app.hr.employee.models import Employee
from client_app.models import BaseModel, TableModel
from datetime import date

# Create your models here.

# class Overtime(BaseModel):
#     name = models.CharField(null=True, unique=True, default="")
#     applicant = models.ForeignKey(Employee,on_delete=models.DO_NOTHING,null=True, default=None)
#     start_time = models.CharField(max_length=255, default='', blank=True, null=True)
#     end_time = models.CharField(max_length=255, default='', blank=True, null=True)
#     purpose = models.TextField(default='', blank=True, null=True)
#     total_earning = models.FloatField(max_length=255,default=0.00, blank=True, null=True)
#     is_paid = models.IntegerField(default=0, null=True)
#     def __str__(self):
#         return f" {self.name}"
#     class Meta:
#         db_table = 'overtime'

class Staffs_To_Work_This_Overtime (TableModel):
    name = models.CharField (max_length=255, unique=True, null=True)
    employee = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    fullname = models.CharField (max_length=255, default="", null=True)
    cleared = models.IntegerField (default=0, null=True)
    from_date = models.DateField (default=date.today, null=True)
    to_date = models.DateField (default=date.today, null=True)
    date_of_work = models.DateField (default=date.today, null=True)
    
    
    class Meta:
        db_table = 'staffs_to_work_this_overtime'

class Overtime(BaseModel):
    name = models.CharField(null=True, unique=True, default="")
    applicant = models.ForeignKey(Employee,on_delete=models.DO_NOTHING, related_name="applicant_ovt",null=True, default=None)
    fullname = models.CharField (max_length=255, default="", null=True)
    designation = models.CharField (max_length=255, default="", null=True)
    department = models.CharField (max_length=255, default="", null=True)
    application_date = models.DateField (default=date.today, null=True)
    from_date = models.DateField (default=date.today, null=True)
    to_date = models.DateField (default=date.today, null=True)
    requested_hours = models.CharField (max_length=255, default="", null=True)
    supervisor = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, related_name="ovt_supervisor", default=name, null=True)
    supervisor_name = models.CharField (max_length=255, default="", null=True)
    purpose = models.TextField(default='', blank=True, null=True)
    why_working_hours = models.TextField(default='', blank=True, null=True)
    is_approved = models.IntegerField (default=0, null=True)
    staff_to_work_on_overtime = models.ManyToManyField (Staffs_To_Work_This_Overtime, blank=True, default=None)
    staff_id = models.CharField (max_length=255, default="", null=True)

    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'overtime'