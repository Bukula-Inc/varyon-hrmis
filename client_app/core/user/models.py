from django.db import models
from client_app.authentication.models import Lite_User
from client_app.models import BaseModel
from django.utils.timezone import now

# Create your models here.
class Auth_Trail(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(Lite_User, on_delete=models.DO_NOTHING, null=True, default=None)
    email = models.CharField(max_length=255, null=True, default="")
    password = models.CharField(max_length=255, null=True, default="")
    activity_type = models.CharField(max_length=255, null=True, default="Login")
    activity_time = models.CharField(default=now, null=True)
    token = models.TextField(null=True, default="Login")
    first_name = models.CharField(max_length=255, null=True, default="")
    last_name = models.CharField(max_length=255, null=True, default="")
    message = models.CharField(max_length=255, null=True, default="")
    
    class Meta:
        db_table = 'auth_trail'


class Password_Reset(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(default=now, null=True)
    user = models.ForeignKey(Lite_User, on_delete=models.DO_NOTHING, null=True, default=None)
    request_date = models.CharField(default=now, null=True)
    expiry_time = models.CharField(default=now, null=True)
    class Meta:
        db_table = 'password_reset'


class User_Certificate(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(Lite_User, on_delete=models.DO_NOTHING, null=True, default=None)
    
    class Meta:
        db_table = 'user_certificate'
