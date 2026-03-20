from django.db import models
from datetime import date
from client_app.controller.tenant.models import Tenant
from client_app.models import BaseModel, TableModel

class Subscription_Module (TableModel):
    module_name = models.CharField(max_length=255, null=True, default="")
    class Meta: 
        db_table = 'subscription_module'

class Subscription (BaseModel):
    name = models.CharField(max_length=255, unique=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.DO_NOTHING,null=True, default=None)
    frequency = models.CharField(max_length=255, null=True)
    is_active = models.IntegerField(null=True, default=1)
    total_users = models.IntegerField(null=True, default=0)
    total_storage = models.IntegerField(null=True, default=0)
    subscription_from = models.DateField(default=date.today)
    subscription_to = models.DateField(default=date.today)
    subscription_modules = models.ManyToManyField(Subscription_Module, blank=True)
    def __str__(self) -> str:
        return self.name
    class Meta: 
        db_table = 'subscription'