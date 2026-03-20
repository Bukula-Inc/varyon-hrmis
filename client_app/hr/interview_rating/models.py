from datetime import date
from django.db import models
from client_app.authentication.models import Lite_User
from client_app.core.country.models import Country
from client_app.hr.designation.models import Designation
from client_app.hr.interview.models import Interview
from client_app.hr.interview_schedule.models import Interview_Schedule
from client_app.models import BaseModel, TableModel

def return_lst():
    return list

class Skill_Rating(TableModel):
    skill =models.CharField(max_length=255, null=True)
    rating =models.IntegerField(null=True, default=0)
    class Meta:
        db_table = "skill_rating"
        
class Candidate_Qualification(TableModel):
    qualification_type = models.CharField(null=True, default="")
    qualification = models.TextField(null=True, default="")
    class Meta:
        db_table = "candidate_qualification"
class Competess_Assessment_Rating(TableModel):
    competence = models.CharField(max_length=255, null=True, default="")
    has_competence = models.IntegerField(null=True, default=0)
    rating = models.FloatField (default=0.00, null=True)
    class Meta:
        db_table = "competess_assessment_rating"
    
class Practical_Assessment_Rating(TableModel):
    practical_skill = models.CharField(max_length=255, null=True, default="")
    has_practical_skill = models.IntegerField(null=True, default=0)
    rating = models.FloatField (default=0.00, null=True)
    class Meta:
        db_table = "practical_assessment_rating"
        
class Interview_Rating(BaseModel):
    name = models.CharField(max_length=255, null=True, unique=True)
    interview_schedule = models.ForeignKey(Interview_Schedule, on_delete=models.DO_NOTHING, default=None, null=True)
    interview = models.ForeignKey(Interview, on_delete=models.DO_NOTHING, default=None, null=True)
    applicant = models.CharField(max_length=255, null=True, default="")
    interview_type = models.CharField(max_length=255, null=True, default="")
    from_time = models.CharField(max_length=255, default="", null=True)
    to_time = models.CharField(max_length=255, default="", null=True)
    designation = models.ForeignKey(Designation, on_delete=models.DO_NOTHING, null=True, default=None)
    rating_complement = models.CharField(null=True, default="")
    evaluator = models.CharField(null=True, default="")
    feed_back = models.TextField(null=True, default="")
    qualifications_rating = models.ManyToManyField(Candidate_Qualification, blank=True)
    skills_rating = models.ManyToManyField(Skill_Rating, blank=True)
    competence_assessment = models.ManyToManyField(Competess_Assessment_Rating, blank=True)
    practical_rating = models.ManyToManyField(Practical_Assessment_Rating, blank=True)

    # NEW FIELDS
    interviewer =models.ForeignKey(Lite_User, on_delete=models.DO_NOTHING, default=None, null=True, related_name="interview_rating_interviewer")
    interviewer_name =models.CharField(max_length=255, default="", null=True)
    interviewer_job_title =models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None, null=True, related_name="interview_rating_interviewer_job_title")
    offered_job_title =models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None, null=True, related_name="interview_rating_offered_job_title")
    applicant_email =models.CharField(max_length=255, default="", null=True)
    applicant_nationality =models.ForeignKey(Country, on_delete=models.DO_NOTHING, default="", null=True, related_name="interview_rating_applicant_nationality")
    nationality_registration_number =models.CharField(max_length=255, default="", null=True)
    technical_total =models.FloatField(default=0.00, null=True)
    behavioral_total =models.FloatField(default=0.00, null=True)
    overall_total =models.FloatField(default=0.00, null=True)
    candidates_suitability =models.CharField(max_length=255, default="", null=True)

    technical_competence = models.JSONField(default=return_lst(), null=True)
    behavioral_competence = models.JSONField(default=return_lst(), null=True)
    other_relevant_information = models.JSONField(default=return_lst(), null=True)
    # interviewer 


    def __str__(self):
        return self.name
    class Meta:
        db_table = "interview_rating"