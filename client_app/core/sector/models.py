from django.db import models

from client_app.models import BaseModel, TableModel

class Sector(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    market_size = models.CharField(max_length=255, null=True, default="")
    economic_impact = models.TextField(null=True, default="")
    trade_associates = models.TextField(null=True, default="")
    key_players = models.TextField(null=True, default="")
    test_data = models.TextField(null=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sector'
