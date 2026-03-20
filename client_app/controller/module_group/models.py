from django.db import models
from client_app.models import BaseModel

class Module_Group(BaseModel):
    name = models.CharField(unique=True)
    allow_multi_select = models.IntegerField(default=0, null=True)
    icon = models.CharField(default="", null=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'module_group'
