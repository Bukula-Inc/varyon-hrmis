from datetime import date
from django.db import models

from client_app.core.country.models import Country
from client_app.hr.designation.models import Designation
from client_app.hr.job_advertisement.models import Job_Advertisement
from client_app.core.currency.models import Currency
from client_app.models import BaseModel, TableModel


class Application_Attachment(TableModel):
    qualification = models.TextField(default="", null=True,blank=True)
    qualification_type = models.CharField(default="", null=True, max_length=255)
    class Meta:
        db_table = 'application_attachment'


class Job_Application_Skill (TableModel):
    skill = models.CharField(max_length=255, default="", null=True)
    has_skill = models.IntegerField(default=0, null=True)
    class Meta:
        db_table = 'job_skills'

class Job_Application(BaseModel):
    name = models.CharField( null=True, unique=True)
    applicant_name = models.CharField(max_length=255,default="",null=True)
    applicant_last_name = models.CharField(max_length=255,default="",null=True)
    applicant_first_name = models.CharField(max_length=255,default="",null=True)
    applicant_middle_name = models.CharField(max_length=255,default="",null=True)
    id_nrc = models.CharField(null=True, default="")
    job_advertisement = models.ForeignKey(Job_Advertisement, on_delete=models.DO_NOTHING, default=None,null=True)
    designation = models.ForeignKey(Designation,on_delete=models.DO_NOTHING, default=None,null=True)
    country = models.ForeignKey(Country,on_delete=models.DO_NOTHING, default=None,null=True)
    email = models.CharField(max_length=255,default="",null=True)
    postal_address = models.CharField(max_length=255, null=True, default="")
    physical_address = models.CharField(max_length=255, null=True, default="")
    date_of_birth = models.DateField(null=True, default=date.today)
    marital_status = models.CharField(max_length=255, null=True, default="")
    mobile = models.CharField(max_length=255,default="",null=True)
    gender = models.CharField(max_length=255, null=True, default="")
    other_names = models.CharField(max_length=255, null=True, default="")
    cover_letter = models.TextField(default="",null=True)
    police_clearance = models.TextField(null=True, default="")
    medical_clearance = models.TextField(null=True, default="")
    applicant_attachement =models.ManyToManyField(Application_Attachment, blank=True)
    job_skills =models.ManyToManyField(Job_Application_Skill, blank=True)
    currency= models.ForeignKey(Currency,on_delete=models.DO_NOTHING, default=None,null=True)  
    lower_range = models.IntegerField(default=0, null=True)
    upper_range = models.IntegerField(default=0,null=True)
    application_initial_score_qualification = models.FloatField (default=0.00, null=True)
    application_initial_score_skill = models.FloatField (default=0.00, null=True)
    letter =models.TextField(default="", null=True)

    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'job_application'


