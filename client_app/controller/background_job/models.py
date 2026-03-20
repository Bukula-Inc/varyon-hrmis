from django.db import models
from client_app.models import BaseModel

class Background_Job(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    module = models.CharField(max_length=255, null=True, default="")
    def __str__(self) -> str:
        return self.name
    class Meta: 
        db_table = 'background_job'