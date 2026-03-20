from django.db import models


from client_app.models import BaseModel
from client_app.core.department.models import Department
from datetime import date




class Company_Policy(BaseModel):
    name = models.CharField(unique=True, max_length=255, null=True)
    department= models.ForeignKey(Department,on_delete=models.DO_NOTHING, default=None, null=True)
    effective_on = models.DateField(default=date.today, null=True)
    purpose_of_policy= models.CharField(max_length=255,default="",null=True)
    policy_context = models.TextField(max_length=255,default="",null=True)
    
    
    
    
    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'company_policy' 


