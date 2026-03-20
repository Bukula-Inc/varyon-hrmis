from django.db import models
from client_app.models import BaseModel, TableModel

# class Leave_Settings (TableModel):


class HR_Text_Template(BaseModel):
    name = models.CharField(unique=True, max_length=255, null=True)
    text_content = models.TextField(null=True, default="")
    
    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'hr_text_template'


