from django.db import models
from client_app.core.company.models import Company
from client_app.hr.employee.models import Employee
from client_app.models import BaseModel, TableModel

# Create your models here.\
class Skill_Levy_Entitled(TableModel):
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    full_name = models.CharField(null=True, max_length=255, default="")
    designation = models.CharField(max_length=255, null=True, default="")
    basic_pay = models.CharField(max_length=255, null=True, default="")
    class Meta:
        db_table = 'skill_levy_entitled'
class Skill_Levy(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    levy_percentage = models.FloatField(null=True, default=0.00)
    enabled = models.IntegerField(null=True, default=0)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, default=None)
    skill_levy_entitled = models.ManyToManyField(Skill_Levy_Entitled, default=None, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table= "skill_levy"
        
    