from django.db import models
from client_app.models import BaseModel

# Create your models here.
class Template_Content(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True, default="")
    template_type = models.CharField(max_length=255, null=True, default="")
    content = models.TextField(null=True)