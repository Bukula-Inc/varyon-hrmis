from django.db import models
from client_app.controller.tenant.models import Tenant
from client_app.models import BaseModel

class License(BaseModel):
    name = models.CharField(unique=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.DO_NOTHING, default=None, null=True, related_name="li_tenant")
    content = models.TextField(null=True, default="",)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'license'
