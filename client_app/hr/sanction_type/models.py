from django.db import models

# Create your models here.
from client_app.models import BaseModel


class Sanction_Type(BaseModel):
    name =models.CharField(max_length=255, default="", null=True)
    active_period =models.IntegerField(default=0, null=True)
    disciplinary_nature =models.CharField(max_length=255, default="", null=True)
    description =models.TextField(default="", null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table ="sanction_type"