from datetime import date
from django.db import models
from client_app.hr.designation.models import Designation
from client_app.models import BaseModel, TableModel

# Create your models here.
class Document(TableModel):
    qualification = models.TextField(default="", null=True,blank=True)
    qualification_type = models.CharField(default="", null=True, max_length=255)
    class Meta:
        db_table = 'document'

class Applicant_Skill(TableModel):
    skill = models.TextField(default="", null=True,blank=True)
    has_skill = models.IntegerField(default=0, null=True)
    class Meta:
        db_table = 'applicant_skill'
class Applicant_Short_List(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    applicant_first_name = models.CharField(max_length=255, null=True, default="")
    applicant_middle_name = models.CharField(max_length=255, null=True, default="")
    applicant_last_name = models.CharField(max_length=255, null=True, default="")
    applicant = models.CharField(max_length=255, null=True, default="")
    applicant_email = models.EmailField(max_length=255, null=True, default="")
    contact_no = models.CharField(max_length=255, null=True, default="")
    job_position = models.ForeignKey(Designation, on_delete=models.DO_NOTHING, null=True, default=None)
    application_date = models.DateField(null=True, default=date.today)
    salary_expectation = models.FloatField(null=True, default=0.00)
    applicant_skills = models.ManyToManyField(Applicant_Skill, blank=True)
    document_files = models.ManyToManyField(Document, blank=True)
    application =models.CharField(max_length=255, default="", null=True)
    job_advertisement =models.CharField(max_length=255, default="", null=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = "applicant_short_list"
    