from django.db import models
from client_app.core.department.models import Department
from client_app.hr.employee.models import Employee
from client_app.models import BaseModel

# Create your models here.

class Transport_Request(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    applicant = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=None, null=True)
    full_name = models.CharField(max_length=255, null=True, default="")
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=None, null=True)
    duration = models.CharField(max_length=255, null=True, default="")
    hours = models.CharField(max_length=255, null=True, default="")
    days =models.CharField(max_length=255, null=True, default="")
    transport_purpose = models.TextField(null=True, default="")
    transport_details = models.JSONField(default=list, blank=True)
    vehicle_allocated =models.CharField(max_length=255, default=True, null=True)
    
    def __str__(self):
        return self.name
    class Meta:
        db_table="transport_request"