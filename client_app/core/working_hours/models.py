from django.db import models
from client_app.models import BaseModel

# Create your models here.
class Main_Working_Hours (BaseModel):
    name = models.CharField (max_length=120, default='', null=True, unique=True)
    opening_time = models.CharField (max_length=120, default='', null=True)
    closing_time = models.CharField (max_length=120, default='', null=True)

    def __str__(self) -> str:
        return self.name
    
    db_table = 'main_working_hours'