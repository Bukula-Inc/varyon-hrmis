from django.db import models
from client_app.core.country.models import Country
from client_app.hr.designation.models import Designation
from client_app.hr.interview.models import Interview
from client_app.hr.job_application.models import Job_Application
from client_app.core.company.models import Company
from client_app.models import BaseModel, TableModel
from datetime import date

def default_json_data():
    return list

class Job_Offer_Entitlement_List(TableModel):
    entitlement =models.CharField(max_length=255, default="", null=True)
    entitlement_amount =models.FloatField(default=0.00, null=True)
    frequency =models.CharField(max_length=255, default="", null=True)

    class Meta:
        db_table ="job_offer_entitlement_list"

class Job_Offer(BaseModel):
    name =models.CharField(max_length=255, null=True, unique=True)
    from_date = models.DateField (default=date.today, null=True)
    to_date = models.DateField (default=date.today, null=True)
    interview = models.ForeignKey(Interview, on_delete=models.DO_NOTHING, default=None, null=True)
    applicant_name = models.CharField(max_length=255,null=True,default="")
    applicant_email = models.CharField(max_length=255,null=True,default="")
    offer_date = models.DateField(default=date.today,null=True)
    offer_due_date = models.DateField(default=date.today,null=True)
    designation = models.ForeignKey(Designation,on_delete=models.DO_NOTHING, default=None,null=True)
    company = models.ForeignKey(Company,on_delete=models.DO_NOTHING, default=None,null=True) 
    terms_and_conditions = models.TextField(blank=True,default="")
    accepted = models.CharField(max_length=255, null=True, default="")
    applicant_contact_info =models.CharField(max_length=255, default="", null=True)
    location =models.CharField(max_length=255, default="", null=True)
    salary =models.FloatField(default=0, null=True)
    grade =models.CharField(max_length=255, default="", null=True)
    pension_scheme =models.CharField(max_length=255, default="", null=True)
    housing_allowance =models.FloatField(default=0, null=True)
    transport_allowance =models.FloatField(default=0, null=True)
    medical_scheme =models.CharField(max_length=255, default=None, null=True)
    hr_hod =models.CharField(max_length=255, default="", null=True)

    # NEW
    entitlements_of_service =models.ManyToManyField(Job_Offer_Entitlement_List, blank=True)
    working_hours =models.JSONField(default=default_json_data(), null=True)
    job_application =models.ForeignKey(Job_Application, on_delete=models.DO_NOTHING, default=None, null=True)


    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'job_offer'
