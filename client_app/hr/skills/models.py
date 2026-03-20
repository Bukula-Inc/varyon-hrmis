from django.db import models
from client_app.models import BaseModel

# Create your models here.
class Skills(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    skill_qualification = models.CharField(max_length=255, null=True, default="")
    category = models.CharField(max_length=255, null=True, default="")
    description = models.TextField(null=True, default="")
    def __str__(self):
        return self.name
    class Meta:
        db_table="skills"
    
    
