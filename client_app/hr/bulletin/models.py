from django.db import models


from client_app.models import BaseModel
from client_app.core.department.models import Department




class Bulletin(BaseModel):
    name = models.CharField(unique=True, null=True,max_length=255, default="")
    bulletin_context = models.TextField(max_length=255,default="")
    attachment =models.TextField(default="", null=True)
    def __str__(self):
        return f" {self.name}"
    class Meta:
        db_table = 'bulletin' 


