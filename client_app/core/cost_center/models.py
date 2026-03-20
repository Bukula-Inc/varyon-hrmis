from django.db import models
from client_app.core.company.models import Company

from client_app.models import BaseModel

# Create your models here.
class Cost_Center(BaseModel):
    name = models.CharField(unique=True, null=True)
    parent_cost_center = models.ForeignKey('self',on_delete=models.DO_NOTHING, null=True, blank=True)
    # project =models.ForeignKey(Project,on_delete=models.DO_NOTHING, null=True, blank=True)
    company = models.ForeignKey(Company,on_delete=models.DO_NOTHING, null=True)
    is_group = models.IntegerField(default=0, null=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'cost_center'