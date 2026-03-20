from django.db import models
from datetime import date

from client_app.hr.designation.models import Designation
from client_app.hr.interview_type.models import Interview_Type
from client_app.hr.job_advertisement.models import Job_Advertisement
from client_app.hr.job_application.models import Job_Application
from client_app.hr.interview_panel.models import Interview_Panel
from client_app.authentication.models import Lite_User
from client_app.hr.short_listed_applicants.models import Applicant_Short_List
from client_app.models import BaseModel , TableModel
from datetime import date

class Applicants_Schedule_List (TableModel):
    application = models.ForeignKey(Applicant_Short_List, on_delete=models.DO_NOTHING, default=None, null=True, )
    position = models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None, null=True, )
    interview_date = models.DateField(default=date.today, null=True)
    form_time = models.CharField(max_length=255,default="", null=True)
    to_time = models.CharField(max_length=255,default="", null=True)
    applicant = models.CharField(max_length=255,default="", null=True)
    applicant_email = models.CharField(max_length=255,default="", null=True)
    class Meta:
        db_table = 'applicants_schedule_list'

class Internal_Interviewers_Schedule (TableModel):
    interviewer_last_name = models.CharField(max_length=255,default="", null=True)
    interviewer_first_name = models.CharField(max_length=255,default="", null=True)
    interviewer_email = models.ForeignKey(Lite_User, on_delete=models.DO_NOTHING, default=None, null=True, )
    class Meta:
        db_table = 'internal_interviewers_schedule'

class External_Interviewers_Schedule(TableModel):
    interviewer_last_name = models.CharField(max_length=255,default="", null=True)
    interviewer_first_name = models.CharField(max_length=255,default="", null=True)
    interviewer_email = models.CharField (max_length=255, default="", null=True)
    class Meta:
        db_table = 'external_interviewers_schedule'


class Interview_Schedule(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True, default="")
    interview_type = models.ForeignKey(Interview_Type, on_delete=models.DO_NOTHING, default=None, null=True, )  # HAS TO GO
    schedule= models.DateField(default=date.today, null=True)
    physical_interview = models.IntegerField(null=True, default=1)
    designation = models.ForeignKey(Designation, on_delete=models.DO_NOTHING, default=None, null=True)
    virtual_interview = models.IntegerField(null=True, default=0)
    link_to_virtual_meeting = models.CharField(max_length=255, null=True, default="")
    from_time =models.CharField(max_length=255, default='', blank=True, null=True)
    to_time= models.CharField(max_length=255, default='', blank=True, null=True)
    application = models.ForeignKey(Job_Application, on_delete=models.DO_NOTHING, default=None, null=True, )
    location = models.CharField (max_length=255, default="", null=True)
    panel_type = models.CharField (max_length=255, default="", null=True)
    internal_interviewers= models.ManyToManyField(Internal_Interviewers_Schedule, blank=True)
    external_Interviewers = models.ManyToManyField(External_Interviewers_Schedule, blank=True)
    applicants_list = models.ManyToManyField(Applicants_Schedule_List, blank=True)
    applicant = models.CharField(max_length=255, null=True, default="")
    schedule_for = models.CharField (max_length=255, default="", null=True)
    link_panel = models.ForeignKey(Interview_Panel, on_delete=models.DO_NOTHING, default=None, null=True, )
    job_advertisement =models.ForeignKey(Job_Advertisement, on_delete=models.DO_NOTHING, default=None, null=True,)
    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'interview_schedule'