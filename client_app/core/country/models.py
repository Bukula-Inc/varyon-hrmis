from django.db import models

from client_app.models import BaseModel

# Create your models here.
class Country(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    code = models.CharField(max_length=50, null=True, default="")
    time_format = models.CharField(max_length=50, null=True, default="")
    time_zones = models.TextField(null=True, default="")
    date_format = models.CharField(max_length=50, null=True, default="")
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'country'