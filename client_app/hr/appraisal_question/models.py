from django.db import models
from client_app.models import BaseModel, TableModel

        
class Appraisal_Question_Option(TableModel):
    name = models.CharField(max_length=255, default="",null=True)
    rate = models.FloatField(default="",null=True)
    class Meta:
        db_table = 'appraisal_question_option'

class Open_Ended_Question(BaseModel):
    name = models.CharField(max_length=255, default="", null=True)
    include_in_self_rating = models.IntegerField(default=0, null=True)
    include_in_360 = models.IntegerField(default=0, null=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'open_ended_question'

class Closed_Ended_Question(BaseModel):
    name = models.CharField(max_length=255, default="", null=True)
    include_in_self_rating = models.IntegerField(default=0, null=True)
    include_in_360 = models.IntegerField(default=0, null=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'closed_ended_question'