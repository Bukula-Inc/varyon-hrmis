from django.db import models


from client_app.models import BaseModel




class Appraisal_Quarter(BaseModel):
    name = models.CharField(unique=True, default="", max_length=255, null=True)
    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'appraisal_quarter' 

