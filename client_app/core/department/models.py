from django.db import models

from client_app.core.company.models import Company
from client_app.core.cost_center.models import Cost_Center
from client_app.authentication.models import Lite_User
from client_app.models import BaseModel




class Department(BaseModel):
    name = models.CharField(unique=True, null=True)
    head_of_department =models.ForeignKey(Lite_User, null=True, on_delete=models.DO_NOTHING, default=None, related_name="head_of_department")
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, default=None, null=True)
    cost_center = models.ForeignKey(Cost_Center, on_delete=models.DO_NOTHING, default=None, null=True)
    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'department'