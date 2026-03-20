from client_app.authentication.models import Lite_User
from client_app.hr.employee.models import Employee
from client_app.models import BaseModel, TableModel
from django.db import models

class Commission_Entry(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True, default=None)
    sales_person = models.ForeignKey(Lite_User, on_delete=models.DO_NOTHING, null=True, default=None, related_name='sales_person_commission')
    reference = models.CharField(max_length=255,default="", null=True)
    inclusive_amount = models.DecimalField(max_digits=10,decimal_places=2, default=0.0, null=True)
    commission_amount = models.CharField(max_length=255,default="", null=True)
    commission_type = models.CharField(max_length=255,default="", null=True)
    service_or_product = models.CharField(max_length=255,default="", null=True) 
    staff_id = models.CharField (max_length=255, default="", null=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta: 
        db_table = 'commission_entry'