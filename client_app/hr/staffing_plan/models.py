from django.db import models


from client_app.models import BaseModel , TableModel

from client_app.core.company.models import Company
from client_app.core.department.models import Department
from client_app.hr.designation.models import Designation
from datetime import date

class Staffing(TableModel):
    designation = models.ForeignKey( Designation, on_delete=models.DO_NOTHING, default=None, null=True)
    department = models.ForeignKey( Department, on_delete=models.DO_NOTHING, default=None, null=True,)
    vacancies = models.CharField(max_length=255,default=0)
    from_date = models.DateField(default=date.today)
    to_date = models.DateField(default=date.today)
    estimated_cost = models.CharField(max_length=255,default=0)
    total_cost = models.CharField(max_length=255,default=0)

    def __str__(self):
        return f" {self.designation}"
    class Meta:
        db_table = 'staffing'


class Staffing_Plan (BaseModel):
    name = models.CharField(null=True, unique=True)
    from_date = models.DateField(default=date.today)
    to_date = models.DateField(default=date.today)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, default=None)
    create_job_offers = models.IntegerField(default=0, null=True)
    publish_job_offer = models.IntegerField(default=0, null=True)
    publish_salary = models.IntegerField(default=0, null=True)
    total_estimated = models.CharField(max_length=255,default=0)
    staffing_details = models.ManyToManyField(Staffing, blank=True)

    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'staffing_plan'



