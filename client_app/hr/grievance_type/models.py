from django.db import models
from django.utils import timezone
from datetime import date


from client_app.models import BaseModel


class Grievance_Type(BaseModel):
    name = models.CharField(max_length=255, default="", null=True)
    description = models.CharField(max_length=255, default="", null=True)
    class Meta:
        db_table = 'grievance_type'
    def __str__(self):
        return self.name