from django.db import models

from client_app.hr.employment_type.models import Employment_Type
from client_app.models import BaseModel, TableModel
from client_app.hr.bonus_types.models import Bonus_Type

class Bonus_Eligibility_Criteria (TableModel):
    employment_Type = models.ForeignKey (Employment_Type, on_delete=models.DO_NOTHING, default=None, null=True) 
    maximum_service_period = models.IntegerField (default=0, null=True)
    service_period_measure = models.CharField (max_length=100, default="", null=True)
    def __str__(self) -> str:
        return self.employment_Type.name
    
    class Meta:
        db_table = 'bonus_eligibility_criteria'

class Bonus_Type_Config (TableModel):
    bonus_type = models.ForeignKey (Bonus_Type, related_name="type_of_bonus", on_delete=models.DO_NOTHING, default=None)


class Bonus_Setting (BaseModel):
    name = models.CharField(max_length=255, unique = True, default="", null=True)
    bonus_types = models.ManyToManyField (Bonus_Type_Config, blank=True)
    eligibility = models.ManyToManyField (Bonus_Eligibility_Criteria, blank=True)
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = 'bonus_setting'