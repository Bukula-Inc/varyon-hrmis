from django.db import models

from client_app.models import BaseModel




class Interview_Type(BaseModel):
    name = models.CharField( null=True, unique=True, default="")
    description = models.CharField(max_length=255,null=True, default="")
    

    
    
    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'interview_type' 


