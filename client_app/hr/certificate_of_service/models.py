from django.db import models
from client_app.core.company.models import Company
from client_app.hr.designation.models import Designation
from client_app.hr.employee.models import Department, Employee
from client_app.hr.employee_separation.models import Employee_Seperation
from client_app.models import BaseModel
from datetime import date
# Create your models here.

class Certificate_Of_Service(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    employee_name = models.CharField (max_length=255, null=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=True, default=None, related_name="certified_employee")
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.DO_NOTHING, null=True)
    employee_seperation = models.ForeignKey(Employee_Seperation, on_delete=models.DO_NOTHING, null=True, related_name="certificate_of_service_employee_separation")

    nrc = models.CharField(max_length=255, null=True, default="")
    napsa_membership_number = models.CharField(max_length=255, null=True, default="")
    state_occupation = models.CharField(max_length=255, null=True, default="")
    address_of_employer = models.CharField(max_length=255, null=True, default="")
    name_in_full = models.CharField(max_length=255, null=True, default="")
    employer_napsa_account_no = models.CharField(max_length=255, null=True, default="")

    from_date = models.DateField(null=True, default=date.today)
    to_date = models.DateField(null=True, default=date.today)
    submition_date = models.DateField(null=True, default=date.today)
    address_of_employer =models,

    prior_year_statutory = models.FloatField(null=True, default=0.00)
    prior_year_savings = models.FloatField(null=True, default=0.00)
    current_year_statutory = models.FloatField(null=True, default=0.00)
    current_year_savings = models.FloatField(null=True, default=0.00)

    state_occupation = models.TextField (blank=True, null=True, default="")
    name_of_employer = models.CharField(max_length=255, null=True, default="")
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, related_name="cs_company")
    


    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'certificate_of_service' 

class Certificate_of_Service_Temporal_Employee (BaseModel):
    name = models.CharField(max_length=255, unique=True)
    employee_name = models.CharField (max_length=255, default="", null=True)
    employee_id = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, null=True, default=None)
    nrc = models.CharField(max_length=255, default="", null=True)
    napsa_membership_number = models.CharField (default=0, null=True)
    employer_napsa_account_number = models.CharField (default=0, null=True)
    designation = models.CharField(max_length=255, default="", null=True)
    from_date = models.DateField (default=date.today, null=True)
    to_date = models.DateField (default=date.today, null=True)
    name_of_employer = models.CharField(max_length=255, default="", null=True)
    address_of_employer = models.CharField(max_length=255, default="", null=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, related_name="csse_company")
    employer_napsa_account_number = models.CharField (default=0, null=True)
    employee_seperation = models.ForeignKey(Employee_Seperation, on_delete=models.DO_NOTHING, null=True, related_name="certificate_of_service_temporal_employee_separation")

# from_date = models.DateField (default=date.today, null=True)

    class Meta:
        db_table ="certificate_of_service_temporal_employee"