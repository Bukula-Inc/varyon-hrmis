from django.db import models

from client_app.hr.appraisal_quarter.models import Appraisal_Quarter
from client_app.hr.employee.models import Employee
from client_app.core.department.models import Department
from client_app.core.company.models import Company
from client_app.models import BaseModel, TableModel
from datetime import date

class Appraisal_Appraiser(TableModel):
    appraiser = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name='appraisals_given')
    appraiser_first_name = models.CharField(max_length=255, null=True, default="")
    appraiser_last_name = models.CharField(max_length=255, null=True, default="")
    appraiser_email = models.CharField(max_length=255, null=True, default="")
    appraisee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default="", null=True, related_name='appraisals_received')
    appraisee_first_name = models.CharField(max_length=255, null=True, default="")
    appraisee_last_name = models.CharField(max_length=255, null=True, default="")
    appraisee_name = models.CharField(max_length=255, default="", null=True)
    appraisee_email = models.CharField(max_length=255, null=True, default="")
    class Meta:
        db_table = 'appraisal_appraiser'

class Appraisal_Appraisee(TableModel):
    appraisee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name='appraisees')
    appraisee_first_name = models.CharField(max_length=255, null=True, default="")
    appraisee_last_name = models.CharField(max_length=255, null=True, default="")
    appraisee_name = models.CharField(max_length=255, default="", null=True)
    appraisee_email = models.CharField(max_length=255, null=True, default="")
    class Meta:
        db_table = 'appraisal_appraisee'

class Appraisal_Setup(BaseModel):
    name = models.CharField(unique=True, null=True)
    appraisal_type = models.CharField(max_length=255, default="", null=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, default=None, null=True)
    appraisal_closure_date = models.DateField(default=date.today, null=True)
    overall_score = models.FloatField(default=0.00, null=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None, null=True, )
    appraisal_quarter = models.ForeignKey(Appraisal_Quarter, on_delete=models.DO_NOTHING, default=None, null=True)
    include_closed_ended_questions = models.IntegerField(default=0, null=True)
    include_open_ended_questions = models.IntegerField(default=0, null=True)
    appraisers = models.ManyToManyField(Appraisal_Appraiser, blank=True, related_name='appraisal_setups')
    appraisees = models.ManyToManyField(Appraisal_Appraisee, blank=True, related_name='appraisal_setups')
    
    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'appraisal_setup'
   