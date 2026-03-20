from django.db import models
from client_app.controller.tenant.models import Tenant
from client_app.models import BaseModel


class User_Pool(BaseModel):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.DO_NOTHING,null=True,default=None)
    name = models.CharField(max_length=255, null=True, default="")
    username = models.CharField(max_length=255, null=True, default="")
    def __str__(self) -> str:
        return self.name
    class Meta: 
        db_table = 'user_pool'
