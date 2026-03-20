from django.db import models


from client_app.hr.appraisal_quarter.models import Appraisal_Quarter
from  client_app.hr.employee.models import Employee
from client_app.core.department.models import Department
from client_app.models import BaseModel , TableModel
from django.contrib.postgres.fields import JSONField
from client_app.core.company.models import Company
from client_app.hr.appraisal_setup.models import Appraisal_Setup
from datetime import date

def default_json_data():
    return {}

class Appraisal(BaseModel):
    name = models.CharField(unique=True, null=True)
    appraisal_setup = models.ForeignKey(Appraisal_Setup, on_delete=models.DO_NOTHING, default=None, null=True,related_name="appraisal_360_setup")
    appraisee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True,related_name="appform_employee")
    appraisee_name= models.CharField(max_length=255,default="", null=True)
    appraiser = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    appraiser_name= models.CharField(max_length=255,default="", null=True)
    appraisal_date = models.DateField(default=date.today,null=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None, null=True, )
    appraisal_quarter = models.ForeignKey(Appraisal_Quarter, on_delete=models.DO_NOTHING, default=None, null=True)
    open_ended_questions = models.JSONField(default=default_json_data, null=True)   
    closed_ended_questions = models.JSONField(default=default_json_data, null=True)  
    overall_score = models.FloatField(default=0.00, null=True)
    total_questions = models.IntegerField(default=0, null=True)
    total_open_ended_questions = models.IntegerField(default=0, null=True)
    total_closed_ended_questions = models.IntegerField(default=0, null=True)
    total_closed_score = models.FloatField(default=0.00, null=True)
    total_open_score = models.FloatField(default=0.00, null=True)

    staff_id = models.CharField(max_length=255, default="", null=True)

    
    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'appraisal' 



