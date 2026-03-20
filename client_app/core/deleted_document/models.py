from django.db import models
from client_app.authentication.models import Lite_User
from client_app.models import BaseModel


def default_content():
    return {}
# Create your models here.
class Deleted_Document(BaseModel):
    name = models.CharField (max_length=255, unique=True)
    doctype = models.CharField (max_length=255, null=True, default="")
    deleted_by = models.ForeignKey(Lite_User, on_delete=models.DO_NOTHING, default=None, related_name="del_by")
    content = models.JSONField(default=default_content, null=True)
    
    class Meta:
        db_table = 'deleted_document'
