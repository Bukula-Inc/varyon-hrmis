from django.db import models

# Create your models here.
from client_app.core.company.models import Company
from client_app.hr.designation.models import Designation
from client_app.core.department.models import Department
from client_app.core.currency.models import Currency
from client_app.hr.employee.models import Employee
from client_app.hr.employment_type.models import Employment_Type
from client_app.models import BaseModel
from client_app.payroll.employee_grade.models import Employee_Grade
from datetime import date

class Job_Advertisement(BaseModel):
    name = models.CharField( null=True, max_length=255, default="", unique=True)
    designation = models.ForeignKey(Designation,on_delete=models.DO_NOTHING, default=None,null=True, related_name="job_advertisement_designation")
    company = models.ForeignKey(Company,on_delete=models.DO_NOTHING, default=None,null=True, related_name="job_advertisement_company")
    department = models.ForeignKey(Department,on_delete=models.DO_NOTHING, default=None,null=True, related_name="job_advertisement_vacancies")
    vacancies = models.CharField(max_length=255, null=True,blank=True, default="")
    number_required =models.IntegerField(default=0, null=True)
    publish = models.IntegerField(default=0,null=True)
    publish_salary = models.IntegerField(default=0,null=True)
    description = models.TextField(default="", blank=True, null=True)
    currency = models.ForeignKey(Currency,on_delete=models.DO_NOTHING, default=None,null=True, related_name="job_advertisement_currency")  
    lower_range = models.FloatField(default=0.00,null=True)
    upper_range = models.FloatField(default=0.00,null=True)
    origin = models.CharField(max_length=255, default="", null=True)
    source_of_recruitment =models.CharField(max_length=255, default="", null=True)
    salary_grade =models.ForeignKey(Employee_Grade, on_delete=models.DO_NOTHING, default=None, null=True)
    employment_type =models.ForeignKey(Employment_Type, on_delete=models.DO_NOTHING, default=None, null=True)
    supervisor = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True, related_name="suporviser")

    from_date =models.DateField(default=date.today, null=True)
    to_date =models.DateField(default=date.today, null=True)



    def __str__(self):
        return self.name
    class Meta:
        db_table = 'job_advertisement'