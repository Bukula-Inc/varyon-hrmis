from django.db import models

from client_app.models import BaseModel

# Create your models here.
class District(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'district'