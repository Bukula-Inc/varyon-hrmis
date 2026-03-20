from django.db import models

# Create your models here.
from django.db import models
from client_app.controller.module.models import Module
from client_app.core.menu_card.models import Menu_Card
from client_app.models import BaseModel, TableModel
from client_app.controller.module_group.models import Module_Group

class Module_Menu_Card(TableModel):
    menu_card = models.ForeignKey(Menu_Card, on_delete=models.DO_NOTHING, null=True, default=None)
    class Meta:
        db_table = 'module_menu_card'

class Module_Pricing(BaseModel):
    name = models.CharField(max_length=255, null=True, default="")
    module_group = models.ForeignKey(Module_Group, on_delete=models.DO_NOTHING, null=True, default=None)
    module = models.ForeignKey(Module, on_delete=models.DO_NOTHING, null=True, default=None)
    total_cost = models.FloatField(default=0.00, null=True)
    employee_range_from = models.IntegerField(default=0, null=True)
    employee_range_to = models.IntegerField(default=0, null=True)
    menu_cards = models.ManyToManyField(Module_Menu_Card, blank=True)
    class Meta:
        db_table = 'module_pricing'