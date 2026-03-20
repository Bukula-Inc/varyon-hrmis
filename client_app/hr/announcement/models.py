from django.db import models


from client_app.models import BaseModel
from client_app.core.department.models import Department
from datetime import date




class Announcement (BaseModel):
    name = models.CharField(unique=True, null=True, default="")
    name_doc = models.CharField(max_length=255, null=True, default="")
    sender = models.CharField(max_length=255, default="", null=True)
    posting_date= models.DateField(default=date.today, null=True)
    announcement_context = models.TextField(max_length=255,  default="",null=True)
    attachment =models.TextField(default="", null=True)
    dept = models.CharField (max_length=255, default="", null=True)
    desig = models.CharField (max_length=255, default="", null=True)
    role = models.CharField (max_length=255, default="", null=True)
    to = models.CharField (max_length=255, default="", null=True)
    def __str__(self):
        return f"{self.name}"
    class Meta:
        db_table = 'announcement' 


