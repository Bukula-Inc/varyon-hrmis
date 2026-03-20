from django.db import models
from client_app.core.doc_status.models import Doc_Status
from client_app.models import BaseModel, TableModel
from django.contrib.postgres.fields import JSONField

def default_imports():
    return {}

class Data_Importation(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    model = models.CharField(max_length=255, null=True, default="")
    file_url = models.CharField(max_length=255, null=True, default="")
    file_name = models.CharField(max_length=255, null=True, default="")
    initial_status = models.ForeignKey(Doc_Status,on_delete=models.DO_NOTHING,null=True,default=None,related_name="initialtats")
    file_size = models.IntegerField(null=True, default=0)
    total_rows = models.IntegerField(null=True, default=0)
    has_extracted_rows = models.IntegerField(null=True, default=0)
    total_successful = models.IntegerField(null=True, default=0)
    total_failed = models.IntegerField(null=True, default=0)
    file_extension = models.CharField(null=True, default="")
    file_content = models.JSONField(default=default_imports, null=True)
    successful_rows = models.JSONField(default=default_imports, null=True)
    failed_rows = models.JSONField(default=default_imports, null=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'data_importation'
