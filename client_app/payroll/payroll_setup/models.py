from client_app.models import BaseModel
from django.db import models

class Payroll_Setup(BaseModel):
    name = models.CharField(max_length=255, unique=True, default="", null=True)
    def __str__(self) -> str:
        return self.name
    class Meta: 
        db_table = 'payroll_setup'
