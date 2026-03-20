from django.db import models
from client_app.models import BaseModel

class Performance_Behavioral_Imperative (BaseModel):
    name = models.CharField (max_length=255, unique=True)
    is_current = models.IntegerField (default=0)
    expected_behavior = models.TextField (null=True, default="")
    def __str__(self):
        return self.name
    class Meta:

        db_table = 'performance_behavior_imperatives'

class Performance_Key_Area (BaseModel):
    name = models.CharField (max_length=255, unique=True)
    area_type = models.CharField (max_length=255, default="", null=True)
    description = models.TextField (blank=True, default="")
    def __str__(self):
        return self.name
    class Meta:

        db_table = 'performance_key_areas'