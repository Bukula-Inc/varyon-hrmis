from django.db import models
from datetime import date
from client_app.models import BaseModel

class Pay_For_Temps_Or_Seasonal_Employee (BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    from_date = models.DateField(default=date.today, null=True)
    to_date = models.DateField(default=date.today,null=True)
    employee = models.JSONField (default=list, null=True)
    staff_id = models.CharField (default="", max_length=255, null=True)
    is_current = models.IntegerField (default=0, null=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'pay_for_temps_or_seasonal_employee'