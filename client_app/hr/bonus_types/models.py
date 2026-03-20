from django.db import models
from client_app.models import BaseModel, TableModel
from client_app.hr.employment_type.models import Employment_Type  



class Bonus_Eligibility (TableModel):
    employment_type = models.ForeignKey (Employment_Type, on_delete=models.DO_NOTHING, default=None, null=True)
    length_in_service_measure = models.CharField (max_length=100, blank=True, null=True, default='')
    length_in_service = models.IntegerField (default=0, null=True, blank=True)
    def __str__(self) -> str:
        return self.employment_type.name
    
    class Meta:
        db_table = 'bonus_eligibility'


class Bonus_Type (BaseModel):
    name = models.CharField(max_length=255, unique = True, default="", null=True)
    description = models.TextField(blank=True, null=True, default="")
    amount_fixed = models.FloatField (blank=True, null=True, default=0.00)
    is_percentage = models.IntegerField (blank=True, null=True, default=0)
    amount_percentage = models.FloatField (blank=True, null=True, default=0.00)
    enable_bonus_type = models.IntegerField (blank=True, null=True, default=0)
    bonus_frequency = models.CharField(max_length=100, null=True, blank=True, default='')
    payment_timing = models.CharField(max_length=100, null=True, blank=True, default='')
    eligibility_criteria = models.ManyToManyField (Bonus_Eligibility, blank=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = 'bonus_type'