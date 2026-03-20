from django.db import models
from client_app.authentication.models import Lite_User
from client_app.models import BaseModel , TableModel

class Panel_Internal_Interviewer (TableModel):
    interviewer_last_name = models.CharField(default="", null=True)
    interviewer_first_name = models.CharField(default="", null=True)
    interviewer_email = models.ForeignKey(Lite_User, on_delete=models.DO_NOTHING, default=None, null=True, related_name="external_member")
    class Meta:
        db_table = 'panel_internal_interviewers'

class Panel_External_Interviewer(TableModel):
    interviewer_last_name = models.CharField(default="", null=True)
    interviewer_first_name = models.CharField(default="", null=True)
    interviewer_email = models.CharField (max_length=255, default="", null=True)
    class Meta:
        db_table = 'panel_external_interviewers'


class Interview_Panel (BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True, default="")
    chairperson =models.ForeignKey(Lite_User, on_delete=models.DO_NOTHING, default=None, null=True, related_name="chairperson")
    chairperson_full_name =models.CharField(max_length=255, default="", null=True)
    internal_interviewers= models.ManyToManyField(Panel_Internal_Interviewer, blank=True)
    external_Interviewers = models.ManyToManyField(Panel_External_Interviewer, blank=True)

    def __str__(self):
        return f" {self.name}"

    class Meta:
        db_table = 'interview_panel'