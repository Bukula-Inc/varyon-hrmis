from django.db import models

from client_app.models import BaseModel

class Hr_Contract_Type (BaseModel):
    name = models.CharField (max_length=255, unique=True, default="", null=True)
    is_short_term = models.IntegerField(default=0, null=True)
    is_graduate_applicable = models.IntegerField (default=0, null=True)
    description = models.TextField (default="", null=True)

    class Meta:
        db_table = "hr_contract_types"

    def __str__(self) -> str:
        return self.name