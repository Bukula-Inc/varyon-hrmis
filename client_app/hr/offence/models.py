from django.db import models

# Create your models here.
from client_app.hr.offence_category.models import Offence_Category
from client_app.models import BaseModel
from client_app.hr.sanction_type.models import Sanction_Type


class Offence(BaseModel):
    name =models.CharField(max_length=255, default="", null=True)
    first_breach =models.ForeignKey(Sanction_Type, on_delete=models.DO_NOTHING, default=None, null=True, related_name="offence_first_breach")
    second_breach =models.ForeignKey(Sanction_Type, on_delete=models.DO_NOTHING, default=None, null=True, related_name="offence_second_breach")
    third_breach =models.ForeignKey(Sanction_Type, on_delete=models.DO_NOTHING, default=None, null=True, related_name="offence_third_breach")
    fourth_breach =models.ForeignKey(Sanction_Type, on_delete=models.DO_NOTHING, default=None, null=True, related_name="offence_fourth_breach")
    category =models.ForeignKey(Offence_Category, on_delete=models.DO_NOTHING, default=None, null=True, related_name="offence_category")

    def __str__(self):
        return self.name

    class Meta:
        db_table ="offence"