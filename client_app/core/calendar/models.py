from django.db import models
from datetime import date

from client_app.models import BaseModel, TableModel

class Calender_Holidays (TableModel):
    month = models.CharField (max_length=20, default='', null=True)
    year = models.CharField (max_length=20, default='', null=True)
    day = models.CharField (max_length=3, default='', null=True)
    date_formate = models.DateTimeField (default=date.today , null=True)
    name_of_holiday = models.CharField (max_length=150, default='', null=True)
    class Meta:
        db_table = 'calendar_holidays'

class Calender (BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True) 
    calendar_holidays = models.ManyToManyField (Calender_Holidays, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'calendar'