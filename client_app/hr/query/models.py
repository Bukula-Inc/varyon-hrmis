from django.db import models

from client_app.hr.employee.models import Employee
from client_app.models import BaseModel
from datetime import date




class Query(BaseModel):
    name = models.CharField(unique=True, max_length=255, null=True)
    employee =  models.ForeignKey(Employee,on_delete=models.DO_NOTHING, default=None,null=True)
    date = models.DateField(default=date.today,null=True)
    subject= models.CharField(max_length=255,null=True,default='')
    context = models.TextField(max_length=255,default='',null=True)
    response = models.TextField(max_length=255, null=True)
    staff_id = models.CharField(max_length=255, default="", null=True)


    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'query'


