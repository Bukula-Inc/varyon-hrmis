from django.db import models
from client_app.models import BaseModel
# Create your models here.
class File_Management(BaseModel):
    name =models.CharField(max_length=255, null=True, default="")
    description =models.TextField(null=True, default="")
    reference_doctype =models.CharField(max_length=255, null=True, default="")
    reference_doc =models.CharField(max_length=255, null=True, default="")
    file_path =models.CharField(max_length=255, null=True, default="")
    file_ext =models.CharField(max_length=255, null=True, default="")
    file_size =models.CharField(max_length=255, null=True, default="")
    class Meta:
        db_table = 'file_management'