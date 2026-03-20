from django.db import models
from django.db import models
from django.utils import timezone
from datetime import date
# Create your models here.
class Doc_Status(models.Model):
    id= models.BigAutoField(primary_key=True)
    created_on = models.DateField(default=date.today, editable=False)
    creation_time = models.DateTimeField(default=timezone.now, editable=False)
    last_modified = models.DateField(default=date.today, editable=False)
    docstatus = models.IntegerField(default=0, null=True)
    initial_docstatus = models.IntegerField(default=0, null=True,)
    doctype = models.CharField(max_length=255, default="Doc_Status", null=True)
    idx = models.IntegerField(default=0, null=True)
    disabled = models.IntegerField(default=0, null=True)
    name = models.CharField(unique=True)
    status_color = models.CharField(max_length=255,default="#C5A0EB", null=True)
    inner_color = models.CharField(max_length=255, default="#610E8C", null=True)
    
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'doc_status'