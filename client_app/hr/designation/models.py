from django.db import models
from client_app.models import BaseModel , TableModel
from client_app.payroll.employee_grade.models import Employee_Grade


class Competess_Assessment(TableModel):
    competess = models.CharField(max_length=255, null=True, default="")
    has_competess = models.IntegerField(null=True, default=0)
    class Meta:
        db_table = "competess_assessment"
    
class Practical_Assessment(TableModel):
    practical_skill = models.CharField(max_length=255, null=True, default="")
    has_practical_skill = models.CharField(null=True, default=0)
    class Meta:
        db_table = "practical_assessment"
class Job_Skill (TableModel):
    skills = models.CharField(max_length=255, null=True, default="")
    must_have = models.IntegerField (default=0, null=True)
    def __str__(self):
        return f" {self.skills}"
    class Meta:
        db_table = 'desig_job_skill'


class Job_Qualification (TableModel):
    qualification = models.CharField(max_length=255, null=True, default="")
    must_have = models.IntegerField (default=0, null=True)
    is_added_advantage = models.IntegerField (default=0, null=True)
    def __str__(self):
        return f" {self.qualification}"
    class Meta:
        db_table = 'desig_job_qualification'


class Designation (BaseModel):
    name = models.CharField(unique=True, max_length=255, null=True)
    department = models.CharField (max_length=255, null=True, default="")
    description = models.TextField(null=True,default="")
    employee_grade = models.ForeignKey (Employee_Grade, on_delete=models.DO_NOTHING, related_name="desig_employee_grade", null=True, default=None)
    skill = models.ManyToManyField(Job_Skill, related_name="desig_job_skills", blank=True)
    qualification = models.ManyToManyField (Job_Qualification, related_name="desig_job_qualifications", blank=True)
    practical_assessment = models.ManyToManyField(Practical_Assessment, blank=True, related_name="practical_assess")
    competess_assessment = models.ManyToManyField(Competess_Assessment, blank=True, related_name="competess_assess")
   
    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'designation'



