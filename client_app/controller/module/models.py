from django.db import models
from datetime import date
from client_app.models import BaseModel
class Module (BaseModel):
    name = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255, null=True, default="")
    icon = models.CharField(max_length=255, null=True, default="")
    url = models.CharField(max_length=255, null=True,default="")
    available = models.CharField(max_length=255, null=True, default="")
    def __str__(self) -> str:
        return self.name
    class Meta: 
        db_table = 'module'