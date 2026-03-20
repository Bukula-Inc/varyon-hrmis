from django.db import models

from client_app.authentication.models import Lite_User
from client_app.models import BaseModel

# Create your models here.


class Onboarding(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True, default="")
    user =models.ForeignKey(Lite_User,on_delete=models.DO_NOTHING,default=None,null=True, related_name="onboard_usr")
    current_stage = models.IntegerField(default=1, null=True)
    splashed = models.IntegerField(default=0, null=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'onboarding'