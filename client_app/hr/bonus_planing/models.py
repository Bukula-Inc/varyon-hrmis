from django.db import models

from client_app.hr.employment_type.models import Employment_Type
from client_app.models import BaseModel, TableModel
from client_app.hr.bonus_types.models import Bonus_Type

class Eligible_Employees (TableModel):
    employment_type = models.ForeignKey (Employment_Type, on_delete=models.DO_NOTHING, default=None)
    length_in_service_measure = models.CharField (max_length=100, blank=True, null=True, default='')
    length_in_service = models.IntegerField (default=0, null=True, blank=True)
    def __str__(self) -> str:
        return self.employment_type.name
    
    class Meta:
        db_table = 'eligibility_employee'
class Bonus_Weightage (TableModel):
    target = models.FloatField (default=0.00, null=True, blank=True)
    of = models.CharField (max_length=100, null=True, blank=True, default='')
    def __str__(self) -> str:
        return self.of
    
    class Meta:
        db_table = 'bonus_weightage'

class Bonus_Threshold (TableModel):
    percentage = models.FloatField (default=0.00, null=True, blank=True)
    of = models.CharField (max_length=100, null=True, blank=True, default='')
    def __str__(self) -> str:
        return self.of
    class Meta:
        db_table = 'bonus_threshold'

class Bonus_Planing (BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True, default='')
    Bonus_Type = models.ForeignKey(Bonus_Type, null=True, blank=True, default=None, on_delete=models.DO_NOTHING)
    payment_timing = models.CharField(max_length=100, null=True, blank=True, default='')
    amount_fixed = models.FloatField (blank=True, null=True, default=0.00)
    is_percentage = models.IntegerField (blank=True, null=True, default=0)
    amount_percentage = models.FloatField (blank=True, null=True, default=0.00)
    maximum_bonus_amount = models.FloatField (blank=True, null=True, default=0.00)
    threshold = models.ManyToManyField (Bonus_Threshold, blank=True)
    eligible_employees = models.ManyToManyField (Eligible_Employees, blank=True)

    class Meta:
        db_table = 'bonus_planing'

    def __str__(self) -> str:
        return self.name