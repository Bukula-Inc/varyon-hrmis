from django.db import models
from client_app.models import BaseModel

class Section(BaseModel):
    name = models.CharField(max_length=255, unique = True, default="")
    description = models.TextField(blank=True, null=True, default="")

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = 'sections'