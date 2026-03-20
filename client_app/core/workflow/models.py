from django.db import models
from client_app.core.department.models import Department
from client_app.core.doc_status.models import Doc_Status
from client_app.core.role.models import Role
from client_app.authentication.models import Lite_User, Lite_User_Group

from client_app.models import BaseModel, TableModel



# Create your models here.
class Workflow_Action(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    icon = models.CharField(max_length=255,default="", null=True)
    color = models.CharField(max_length=255,default="", null=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'workflow_action'


class Workflow_Approver_Role(TableModel):
    approver = models.ForeignKey(Role, on_delete=models.DO_NOTHING, null=True, default=None)
    should_always_be_present = models.IntegerField(default=0, null=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'workflow_approver_role'



class Workflow_Approver_Group(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    minimum_total_approvers = models.IntegerField(default=1, null=True)
    approvers = models.ManyToManyField(Workflow_Approver_Role, blank=False)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'workflow_approver_group'


class Workflow_Stage(TableModel):
    stage = models.ForeignKey(Doc_Status, on_delete=models.DO_NOTHING, null=True, default=None,related_name="wf_stage")
    stage_no = models.IntegerField(null=True, default=0)
    action = models.ForeignKey(Workflow_Action, on_delete=models.DO_NOTHING, null=True, default=None)
    next_stage = models.ForeignKey(Doc_Status, on_delete=models.DO_NOTHING, null=True, default=None,related_name="wf_next_stage")
    approver_group = models.ForeignKey(Workflow_Approver_Group, on_delete=models.DO_NOTHING, null=True, default=None,related_name="wf_ag")
    approver = models.ForeignKey(Lite_User, on_delete=models.DO_NOTHING, null=True, default=None,related_name="lu_approver")
    approver_user_group = models.ForeignKey(Lite_User_Group, on_delete=models.DO_NOTHING, null=True, default=None,related_name="aug")
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'workflow_stage'



class Workflow(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    record_type = models.CharField(max_length=255, unique=False, null=True)
    is_role_based_workflow = models.IntegerField(null=True, default=0)
    is_departmental_workflow = models.IntegerField(null=True, default=0)
    is_user_group_workflow = models.IntegerField(null=True, default=0)
    allow_none_departmental_approvers = models.IntegerField(null=True, default=0)
    allow_non_owner_initialization = models.IntegerField(null=True, default=0)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True, default=None,related_name="wf_dept")
    user_group = models.ForeignKey(Lite_User_Group, on_delete=models.DO_NOTHING, null=True, default=None,related_name="lug")
    workflow_stage = models.ManyToManyField(Workflow_Stage, blank=False)
    
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'workflow'



# track approvers
class Workflow_Doc_Approver(TableModel):
    approver = models.ForeignKey(Role, on_delete=models.DO_NOTHING, null=True, default=None,related_name="wf_dapp_role")
    action_taken = models.CharField(max_length=255, null=True)
    should_always_be_present = models.IntegerField(null=True, default=0)
    def __str__(self):
        return self.name
    class Meta: 
        db_table = 'workflow_doc_approver'


class Workflow_Doc_Approver_Tracker(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    doctype = models.CharField(max_length=255, unique=True, null=True)
    approvers = models.ManyToManyField(Workflow_Doc_Approver, blank=False)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'workflow_doc_approver_tracker'

class Workflow_Doc(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    for_doctype = models.CharField(max_length=255, default="", null=True)
    current_stage = models.ForeignKey(Doc_Status, on_delete=models.DO_NOTHING, related_name="wf_cur_stage", null=True, default=None)
    current_stage_no = models.IntegerField(null=True, default=0)
    comments = models.JSONField(null=True, default=list)
    workflow_used = models.ForeignKey(Workflow, on_delete=models.DO_NOTHING, null=True, default=None,related_name="doc_wf")
    # past_status = models.JSONField(null=True, default=list)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'workflow_doc'