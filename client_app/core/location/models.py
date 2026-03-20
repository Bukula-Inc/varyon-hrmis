from django.db import models

from django.db import models

from client_app.models import BaseModel

# Create your models here.
class Location(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    latitude = models.CharField(max_length=255, unique=True, null=True)
    longitude = models.CharField(max_length=255, unique=True, null=True)
    description = models.TextField(max_length=255, unique=True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'location'