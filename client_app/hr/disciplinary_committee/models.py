from django.db import models
from client_app.hr.charge_form.models import Charge_Form
from client_app.models import BaseModel, TableModel

class Disciplinary_Committee_Member (TableModel):
    member_name = models.CharField (max_length=255, null=True, default='')
    # member_status = models.CharField (default=0, null=True)
    member_email = models.CharField (max_length=255, null=True, default='')
    # member_role_in_committee= models.CharField (max_length=255, null=True, default='')

    def __str__(self):
        return f" {self.member_name}"
    class Meta:
        db_table = 'disciplinary_committee_member' 


class Internal_Disciplinary_Committee_Member (TableModel):
    member_name = models.CharField (max_length=255, null=True, default='')
    # member_status = models.CharField (default=0, null=True)
    member_email = models.CharField (max_length=255, null=True, default='')
    # member_role_in_committee= models.CharField (max_length=255, null=True, default='')

    def __str__(self):
        return f" {self.member_name}"
    class Meta:
        db_table = 'internal_disciplinary_committee_member' 


class External_Disciplinary_Committee_Member (TableModel):
    member_name = models.CharField (max_length=255, null=True, default='')
    member_email = models.CharField (max_length=255, null=True, default='')

    def __str__(self):
        return f" {self.member_name}"
    class Meta:
        db_table = 'external_disciplinary_committee_member' 

class Disciplinary_Committee (BaseModel):
    name = models.CharField (unique=True, max_length=255, null=True)
    members = models.ManyToManyField (Disciplinary_Committee_Member, blank=True)
    internal_members = models.ManyToManyField (Internal_Disciplinary_Committee_Member, blank=True)
    external_members = models.ManyToManyField (External_Disciplinary_Committee_Member, blank=True)
    charge =models.ForeignKey(Charge_Form, on_delete=models.DO_NOTHING, default=None, null=True)

    # NEW
    chairperson =models.CharField(max_length=255, default="", null=True)

    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'disciplinary_committee' 