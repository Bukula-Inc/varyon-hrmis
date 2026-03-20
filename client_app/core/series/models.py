from django.db import models
from django.utils import timezone
from datetime import date
# Create your models here.
class Series(models.Model):
    id= models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, null=True)
    created_on = models.DateField(default=date.today, editable=False)
    creation_time = models.DateTimeField(default=timezone.now, editable=False)
    last_modified = models.DateField(default=date.today, editable=False)
    docstatus = models.IntegerField(default=0, null=True)
    doctype = models.CharField(max_length=255, default="Series", null=True)
    idx = models.IntegerField(default=0, null=True)
    disabled = models.IntegerField(default=0, null=True)
    name_format = models.CharField(max_length=255, null=True)
    series_count = models.IntegerField(null=True, default=1)
    series_digits = models.IntegerField(null=True, default=4)
    
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'series'