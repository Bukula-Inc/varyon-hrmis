from django.db import models
from client_app.models import BaseModel

class Rating (BaseModel):
    name = models.CharField (max_length=255, unique=True, default='')
    subject = models.CharField(max_length=100, default='', null=True)
    rating = models.IntegerField (default=0, blank=True)
    feedback_message = models.TextField (default='', null=True)
    feedback_by = models.CharField (max_length=255, default='', null=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = 'rating'