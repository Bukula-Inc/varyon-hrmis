from django.db import models
from client_app.models import BaseModel

class Branch (BaseModel):
    name = models.CharField (max_length=255, unique=True)
    branch_id = models.CharField (max_length=50, null=True, default="")
    branch_location = models.TextField (blank=True, null=True)
    is_main_branch = models.IntegerField (default=0, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'branch'