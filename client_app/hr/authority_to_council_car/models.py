from django.db import models
from client_app.models import BaseModel
from client_app.hr.employee.models import Employee
from datetime import date

class Request_For_Council_Car (BaseModel):
    name = models.CharField (max_length=255, unique=True)
    employee = models.ForeignKey (Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    drivers_name = models.CharField (max_length=255, default="", null=True)
    drivers_license_number = models.CharField (max_length=30, null=True, default=True)
    drivers_license_class = models.CharField (max_length=30, null=True, default=True)
    drivers_license_expiry_date = models.DateField (null=True, default=date.today)
    travel_date = models.DateField (null=True, default=date.today)
    destination = models.CharField (max_length=30, null=True, default=True)
    self_driving_reason = models.TextField (blank=True)
    purpose = models.TextField (blank=True)
    vehicle_allocated =models.CharField(max_length=255, default="", null=True)
    upload_drivers_license = models.TextField(null=True, default="")

    motor_vehicle_allocated =models.CharField(max_length=255, default=True, null=True)
    staff_id = models.CharField(max_length=255, default="", null=True)
    class Meta:
        db_table = 'request_for_council_car'


    def __str__(self):
        return self.name