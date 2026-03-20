from django.db import models


from client_app.models import BaseModel, TableModel
from client_app.core.company.models import Company
from client_app.hr.training_program.models import Training_Program
from client_app.hr.employee.models import Employee
from datetime import date


class Listed_Training_Plan(TableModel):

    training_program =models.CharField(max_length=255, default="", null=True)
    training_type =models.CharField(max_length=255, default="", null=True)
    course =models.CharField(max_length=255, default="", null=True)
    program_duration =models.CharField(max_length=255, default="", null=True)
    certification_type =models.CharField(max_length=255, default="", null=True)
    description =models.TextField(default="", null=True)
    training_expense =models.IntegerField(default=0, null=True)

    class Meta:
        db_table = 'listed_training_plan'


class Training_Plan(BaseModel):
            
    name =models.CharField(max_length=255, unique=True, default="", null=True)
    company =models.ForeignKey(Company, on_delete=models.DO_NOTHING, default=None, null=True)
    plan_period =models.CharField(max_length=255, default="", null=True)
    from_date =models.DateField(default=date.today, null=True)
    to_date =models.DateField(default=date.today, null=True)
    listed_trianing_plans =models.ManyToManyField(Listed_Training_Plan, blank=True)
    description =models.TextField(default="", null=True)
    use_status =models.CharField(max_length=255, default="", null=True)

    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'training_plan'


