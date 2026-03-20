from django.db import models

# Create your models here.
from client_app.models import BaseModel


class Offence_Category(BaseModel):
    name =models.CharField(max_length=255, unique=True, default="", null=True)
    title =models.CharField(max_length=255, default="", null=True)
    description =models.TextField(default="", null=True)
    
    class Meta:
        db_table ="offence_category"