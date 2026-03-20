from django.db import models
from client_app.models import BaseModel
from datetime import date
# Create your models here.
class OTP(BaseModel):
    name= models.CharField(max_length=255, unique=False, null=True, default="")
    party_id= models.CharField(max_length=255, null=True, default="")
    email= models.CharField(max_length=255, null=True, default="")
    phone= models.CharField(max_length=255, null=True, default="")
    otp= models.CharField(max_length=255, null=True, default="")
    auth_type = models.CharField(max_length=255, null=True, default="")
    expiry_date = models.DateField(null=True,default=date.today)
    expiry_time = models.CharField(null=True, default="")
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'otp'