from django.db import models
from client_app.models import BaseModel

class Priority(BaseModel):
    name = models.CharField(max_length=255, unique=True,)
    description = models.TextField(null=True, blank=True, default="")
    def __str__(self):
        return self.name
    class Meta:
        db_table="priority"