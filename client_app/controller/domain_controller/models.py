from django.db import models
from client_app.models import BaseModel


class Domain_Controller(BaseModel):
    name = models.CharField(max_length=255, unique=True, default="Domain Controller")
    domain_ip = models.CharField(max_length=255, null=True, default="")
    domain_url = models.CharField(max_length=255, null=True, default="")
    domain_host_url = models.CharField(max_length=255, null=True, default="")
    domain_host_api_key = models.CharField(max_length=255, null=True, default="")
    domain_host_secret_key = models.CharField(max_length=255, null=True, default="")
    domain_default_ttl = models.CharField(max_length=255, null=True, default="")
    domain_default_record_type = models.CharField(max_length=255, null=True, default="")
    def __str__(self) -> str:
        return self.name
    class Meta: 
        db_table = 'domain_controller'