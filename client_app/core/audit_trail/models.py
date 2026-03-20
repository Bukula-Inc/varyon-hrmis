from django.db import models
from client_app.models import BaseModel, TableModel
from datetime import date
from django.utils.timezone import now

class Audit_Item(TableModel):
    action = models.CharField(max_length=255, null=True, default="")
    field = models.CharField(max_length=255, null=True, default="")
    time_created = models.CharField(default=now, null=True)
    before_content = models.TextField(max_length=255, null=True, default="")
    after_content = models.TextField(max_length=255, null=True, default="")
    class Meta:
        db_table = 'audit_item'

# Create your models here.
class Audit_Trail(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    doc_name = models.CharField(max_length=255, null=True, default="")
    document_type = models.CharField(max_length=255, null=True, default="")
    name = models.CharField(max_length=255, null=True, default="")
    audit_items = models.ManyToManyField(Audit_Item, blank=True)
    class Meta:
        db_table = 'audit_trail'
