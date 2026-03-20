from django.db import models


from client_app.models import BaseModel
from datetime import date




class Memo(BaseModel):
    name = models.CharField(unique=True, null=True)
    to = models.CharField(max_length=255,default="",null=True)
    sender = models.CharField(max_length=255,null=True,default="")
    from_desig = models.CharField (max_length=255, null=True, default="")
    date = models.DateField(default=date.today, null=True)
    dept = models.CharField (max_length=255, default="", null=True)
    desig = models.CharField (max_length=255, default="", null=True)
    role = models.CharField (max_length=255, default="", null=True)
    ind = models.CharField (max_length=255, default="", null=True)
    subject = models.CharField(max_length=255,default="",null=True)
    body = models.TextField(max_length=255,default="",null=True)
    attachment =models.TextField(default="", null=True, blank=True)
    recipients = models.JSONField (default=list, null=True) 
    cc = models.TextField (null=True, blank=True)
    custom = models.JSONField (null=True, default=list)

    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'memo'


