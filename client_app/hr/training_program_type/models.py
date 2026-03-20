from django.db import models
from client_app.models import BaseModel
# Create your models here.
class Training_Program_Type(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(null=True, blank=True, default="")

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'training_program_type'

