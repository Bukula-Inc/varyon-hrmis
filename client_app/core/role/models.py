from django.db import models
from client_app.controller.module.models import Module
from client_app.core.default_dashboard.models import Default_Dashboard
from client_app.core.department.models import Department
from client_app.models import BaseModel, TableModel

def default_role_content():
    return []


class Role_Module(TableModel):
    role_module = models.ForeignKey(Module, on_delete=models.DO_NOTHING, null=True, default=None)
    permit_all = models.IntegerField(null=True, default=0)
    default_dashboard = models.ForeignKey(Default_Dashboard, on_delete=models.DO_NOTHING, null=True, related_name="rm_def_d", default=None)
    role_cards = models.JSONField(default=dict, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'role_module'

class Role(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True, default="")
    department = models.ForeignKey(Department, on_delete = models.DO_NOTHING, null=True, default=None)
    default_dashboard = models.ForeignKey(Default_Dashboard, on_delete=models.DO_NOTHING, null=True, default=None)
    module = models.ForeignKey(Module, on_delete=models.DO_NOTHING, null=True, default=None, related_name="rmdl")
    description = models.TextField(null=True, default="")
    role_module = models.ManyToManyField(Role_Module, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'role'
