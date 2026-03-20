from django.db import models
from client_app.models import BaseModel

# Create your models here.
class Background_Job_Results(BaseModel):
    name = models.CharField(max_length=255)
    module = models.CharField(max_length=255, null=True, default="")
    task_name = models.CharField(max_length=255, null=True, default="")
    execution_time = models.CharField(max_length=255, null=True, default="")
    execution_frequency = models.CharField(max_length=255)
    result = models.TextField(null=True,default="")
    error_message = models.TextField(null=True,default="")
    def __str__(self) -> str:
        return self.name
    class Meta: 
        db_table = 'background_job_results'