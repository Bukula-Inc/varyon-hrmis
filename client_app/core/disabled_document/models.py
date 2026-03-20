from django.db import models
from client_app.models import BaseModel
def disabled_field_content():
    return {}
# Create your models here.
class Disabled_Document (BaseModel):
    name = models.CharField (max_length=255, unique=True)
    doc_id = models.IntegerField ( unique=True)
    initial_status = models.CharField (null=True, default="")
    doc_name = models.CharField (null=True, default="")
    document_type = models.CharField (null=True, default="")
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'disabled_document'