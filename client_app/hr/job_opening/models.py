from django.db import models

from client_app.core.company.models import Company
from client_app.hr.designation.models import Designation
from client_app.core.department.models import Department
from client_app.core.currency.models import Currency
from client_app.models import BaseModel




class Job_Opening(BaseModel):
    name = models.CharField( null=True, max_length=255, default="", unique=True)
    designation = models.ForeignKey(Designation,on_delete=models.DO_NOTHING, default=None,null=True)
    company = models.ForeignKey(Company,on_delete=models.DO_NOTHING, default=None,null=True)
    department = models.ForeignKey(Department,on_delete=models.DO_NOTHING, default=None,null=True)
    vacancies = models.CharField(max_length=255, null=True,blank=True, default="")
    publish = models.IntegerField(default=0,null=True)
    publish_salary = models.IntegerField(default=0,null=True)
    description = models.TextField(default="", blank=True, null=True)
    currency = models.ForeignKey(Currency,on_delete=models.DO_NOTHING, default=None,null=True)  
    lower_range = models.FloatField(default=0.00,null=True)
    upper_range = models.FloatField(default=0.00,null=True)

    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'job_opening'
