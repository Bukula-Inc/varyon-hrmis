from django.db import models
from datetime import date
from client_app.controller.module.models import Module
from client_app.controller.module_pricing.models import Module_Pricing
from client_app.models import TableModel

class Tenant_Module_Pricing(TableModel):
    module_price = models.ForeignKey(Module_Pricing, on_delete=models.DO_NOTHING,null=True,default=None)
    module = models.ForeignKey(Module, on_delete=models.DO_NOTHING,null=True,default=None, related_name="tntmdl")
    is_suspended = models.IntegerField(null=True, default=0)
    class Meta: 
        db_table = 'tenant_module_pricing'

class Tenant (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    docstatus = models.IntegerField(null=True,default=0)
    db_name = models.CharField(max_length=255, null=True)
    db_user = models.CharField(max_length=255, null=True)
    db_password = models.TextField(null=True)
    api_key = models.TextField(null=True, default="")
    db_host = models.CharField(max_length=255, null=True)
    db_port = models.CharField(max_length=255, null=True)
    tenant_url = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, null=True)
    created_on = models.DateField(default=date.today, null=True)
    expiry_date = models.DateField(default=date.today, null=True)
    total_users = models.IntegerField(null=True)
    total_storage = models.IntegerField(null=True)
    license_no = models.CharField(max_length=255, null=True)
    subscription_frequency = models.CharField(max_length=255, null=True, default="Annually")
    modules = models.ManyToManyField(Tenant_Module_Pricing, blank=True)
    def __str__(self) -> str:
        return self.name
    class Meta: 
        db_table = 'tenant'
