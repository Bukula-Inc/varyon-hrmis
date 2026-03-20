from django.db import models

from client_app.models import BaseModel

# Create your models here.
class Email_Config(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    server_name = models.CharField(max_length=255, null=True, default="")
    port_no = models.CharField(max_length=255, null=True, default="")
    email_address = models.CharField(max_length=255, null=True, default="")
    email_password = models.CharField(max_length=255, null=True, default="")
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'email_config'