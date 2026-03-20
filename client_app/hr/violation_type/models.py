from django.db import models

from client_app.models import BaseModel




class Violation_Type(BaseModel):
    name = models.CharField( null=True, unique=True)

    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'violation_type'


