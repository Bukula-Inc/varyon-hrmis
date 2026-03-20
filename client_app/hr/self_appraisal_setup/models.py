from django.db import models


from client_app.hr.appraisal_quarter.models import Appraisal_Quarter
from  client_app.hr.employee.models import Employee
from client_app.core.department.models import Department
from client_app.models import BaseModel , TableModel
from datetime import date

class Self_Appraisal_Appraisee(TableModel):
    appraisee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, )
    appraisee_name = models.CharField(max_length=255, null=True, default="")
    appraisee_department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None, null=True, )
    class Meta:
        db_table = 'self_appraisal_appraisee'

class Self_Appraisal_Setup(BaseModel):
    name = models.CharField(unique=True, null=True, default="", max_length=255)
    appraisal_closure_date = models.DateField(default=date.today)
    appraisal_quarter = models.ForeignKey(Appraisal_Quarter, on_delete=models.DO_NOTHING, default=None, null=True )
    include_closed_ended_questions = models.IntegerField(default=0, null=True)
    include_open_ended_questions = models.IntegerField(default=0, null=True)
    appraisees= models.ManyToManyField(Self_Appraisal_Appraisee, blank=True)

    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'self_appraisal_setup'



