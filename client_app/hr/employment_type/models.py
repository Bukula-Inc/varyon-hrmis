from django.db import models
from django.utils import timezone
from datetime import date


from client_app.models import BaseModel


class Employment_Type(BaseModel):
    name = models.CharField(max_length=255, default="", null=True)
    class Meta:
        db_table = 'employment_type'
    def __str__(self):
        return self.name