from django.db import models
from client_app.models import BaseModel, TableModel
from datetime import date
from django.utils.timezone import now

class Field_Config(TableModel):
    field_name = models.CharField(max_length=255, null=True, default="")
    make_mandatory = models.IntegerField(null=True, default=0)
    hide_field = models.IntegerField(null=True, default=0)
    display_on = models.TextField(max_length=255, null=True, default="")
    fetch_from = models.CharField(max_length=255, null=True, default="")
    fetch_field = models.CharField(max_length=255, null=True, default="")
    class Meta:
        db_table = 'field_config'

# Create your models here.
class Form_Customization(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True, default="")
    allow_submit = models.IntegerField(null=True, default=0)
    allow_create = models.IntegerField(null=True, default=0)
    allow_update = models.IntegerField(null=True, default=0)
    allow_cancel = models.IntegerField(null=True, default=0)
    allow_delete = models.IntegerField(null=True, default=0)
    allow_print = models.IntegerField(null=True, default=0)
    allow_duplicate = models.IntegerField(null=True, default=0)
    allow_disable = models.IntegerField(null=True, default=0)
    allow_send_mail = models.IntegerField(null=True, default=0)
    form_title = models.CharField(max_length=255, null=True, default="")
    field_config = models.ManyToManyField(Field_Config, blank=True)
    class Meta:
        db_table = 'form_customization'
