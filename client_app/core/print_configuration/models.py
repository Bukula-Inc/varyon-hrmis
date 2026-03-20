from django.db import models
from client_app.models import BaseModel, TableModel

# Create your models here.
class Print_Configuration_Field(BaseModel):
    field_name = models.CharField(null=True)
    field_type = models.CharField(null=True)
    columns = models.IntegerField(null=True)
    include_in_print = models.CharField(null=True)
    class Meta:
        db_table = 'print_configuration_field'
        
class Print_Configuration(BaseModel):
    name = models.CharField(null=True,unique=True)
    app_model = models.CharField(null=True)
    configuration_fields = models.ManyToManyField(Print_Configuration_Field, blank=True)
    def __date__(self):
        return self.name
    class Meta:
        db_table = 'print_configuration'