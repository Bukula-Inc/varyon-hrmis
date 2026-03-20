from django.db import models
from client_app.authentication.models import Lite_User
from client_app.core.country.models import Country
from client_app.hr.designation.models import Designation
from client_app.models import BaseModel , TableModel
from client_app.hr.interview_schedule.models import Interview_Schedule
from datetime import date
from client_app.hr.short_listed_applicants.models import Applicant_Short_List


def return_lst():
    return list


class Feedback(TableModel):
    evaluator = models.CharField(null=True, default="")
    interview_feedback = models.TextField(default="",null=True)
    average_rating = models.CharField(max_length=255, default="",null=True)
    result = models.TextField(default="", null=True)
    competence = models.FloatField(null=True, default=0.00)
    practical = models.FloatField(null=True, default=0.00)
    class Meta:
        db_table = 'feedback'

class Skill_Assessment(TableModel):
    skill = models.CharField(max_length=255,default="",null=True)
    rating = models.CharField(max_length=255,default="",null=True)   
 
    def __str__(self):
        return f" {self.skill}"
    class Meta:
        db_table = 'skill_assessment'

class Interview_Qualification (TableModel):
    qualification = models.TextField(default="",blank=True, null=True)  
    qualification_type = models.CharField(max_length=255, null=True, default=True)
 
    def __str__(self):
        return f"Interview {self.qualification}"
    class Meta:
        db_table = 'interview_qualification'

class Interview(BaseModel):
    name = models.CharField(null=True, unique=True, default="")
    interview_schedule = models.ForeignKey(Interview_Schedule, on_delete=models.DO_NOTHING, default=None, null=True)
    short_listed_applicant = models.ForeignKey(Applicant_Short_List, on_delete=models.DO_NOTHING, null=True, default=None)
    designation = models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None, null=True)
    email = models.CharField(null=True, default="")
    contact_no = models.CharField(null=True, default="")
    interview_type = models.CharField(null=True, default="")
    application_outcome = models.CharField(max_length=255, default='', blank=True, null=True)
    schedule = models.DateField(default=date.today, null=True)
    from_time = models.CharField(max_length=255, default='', blank=True, null=True)
    to_time = models.CharField(max_length=255, default='', blank=True, null=True)
    applicant = models.CharField(null=True, default='')
    interview_summary = models.TextField(default='', blank=True,null=True)
    feedback = models.ManyToManyField(Feedback, blank=True)
    skills = models.ManyToManyField(Skill_Assessment, blank=True)
    qualifications = models.ManyToManyField (Interview_Qualification, blank=True)

    # NEW FIELDS
    offered_job_title =models.ForeignKey(Designation, on_delete=models.DO_NOTHING, null=True, default=None, related_name="offered_job_title_interview")
    applicant_email =models.CharField(max_length=255, default="", null=True)
    applicant_nationality =models.ForeignKey(Country, on_delete=models.DO_NOTHING, default=None, null=True, related_name="applicant_nationality_interview")
    nationality_registration_number =models.CharField(max_length=255, default="", null=True)
    technical_total =models.FloatField(default=0.00, null=True)
    behavioral_total =models.FloatField(default=0.00, null=True)
    overall_total =models.FloatField(default=0.00, null=True)
    candidates_suitability =models.CharField(max_length=255, default="", null=True)

    technical_competence = models.JSONField(default=return_lst(), null=True)
    behavioral_competence = models.JSONField(default=return_lst(), null=True)
    other_relevant_information = models.JSONField(default=return_lst(), null=True)

    
    
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        db_table = 'interview'



