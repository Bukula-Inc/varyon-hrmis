from django.db import models
from client_app.models import BaseModel, TableModel
from django.contrib.postgres.fields import JSONField

def child_items_json():
    return []

class Menu_Card_Item(TableModel):
    title = models.CharField(max_length=255, null=True, default="")
    module = models.CharField(max_length=255, null=True, default="")
    app = models.CharField(max_length=255, null=True, default="")
    page_type = models.CharField(max_length=255, null=True, default="")
    content_type = models.CharField(max_length=255, null=True, default="")
    child_items = models.JSONField(default=child_items_json, null=True)
    icon = models.TextField(max_length=255, null=True, default="")
    display = models.IntegerField(null=True, default=0)
    class Meta:
        db_table = 'menu_card_item'

# Create your models here.
class Menu_Card(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    module = models.CharField(max_length=255, null=True, default="")
    card_items = models.ManyToManyField(Menu_Card_Item, blank=True)
    
    class Meta:
        db_table = 'menu_card'
