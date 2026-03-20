from django.db import models
from client_app.controller.module.models import Module
from client_app.core.menu_card.models import Menu_Card
from client_app.models import BaseModel, TableModel

class Allowed_Menu(TableModel):
    menu_card = models.ForeignKey(Menu_Card, on_delete=models.DO_NOTHING, null=True,default=None)
    
    class Meta:
        db_table = 'allowed_menu'

# Create your models here.
class Default_Dashboard (BaseModel):
    name = models.CharField (max_length=255, unique=True)
    module = models.ForeignKey(Module, on_delete=models.DO_NOTHING, default=None, null=True)
    app_name = models.CharField(max_length=255, default= "", null=True)
    page_type = models.CharField(max_length=255, default= "", null=True)
    content_type = models.CharField(max_length=255, default= "", null=True)
    allowed_menus = models.ManyToManyField(Allowed_Menu, blank=True)
    class Meta:
        db_table = 'default_dashboard'