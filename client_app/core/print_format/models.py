from django.db import models
from client_app.models import BaseModel

# Create your models here.
# class Printed_Document(BaseModel):
#     name = models.CharField(max_length=255, null=True, blank=True, default="")
#     document_type =models.CharField(max_length=255, null=True, blank=True, default="")
#     print_count = models.CharField(max_length=255, null=True, blank=True, default="")
#     class Meta:
#         db_table = 'printed_document'
        
class Print_Format(BaseModel):
    name = models.CharField(unique=True, null=True)
    app_model = models.CharField(null=True)
    is_default = models.IntegerField(null=True,default=0)
    html = models.TextField( null=True)
    def __date__(self):
        return self.name
    class Meta:
        db_table = 'print_format'


# Create your models here.
class Printed_Document(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True, default="", unique=True)
    document_type =models.CharField(max_length=255, null=True, blank=True, default="")
    print_count = models.IntegerField(null=True, blank=True, default=0)
    class Meta:
        db_table = 'printed_document'