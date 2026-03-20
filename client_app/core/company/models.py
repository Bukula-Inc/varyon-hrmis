from django.db import models
from client_app.core.city.models import City
from client_app.core.country.models import Country
from client_app.core.currency.models import Currency
from client_app.core.industry.models import Industry
from client_app.core.sector.models import Sector
from client_app.core.state.models import State

from client_app.models import BaseModel

# Create your models here.
class Company(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    industry = models.ForeignKey(Industry,on_delete=models.DO_NOTHING, default=None,null=True)
    sector = models.ForeignKey(Sector,on_delete=models.DO_NOTHING,default=None,null=True)
    country = models.ForeignKey(Country,on_delete=models.DO_NOTHING,default=None, null=True)
    state = models.ForeignKey(State,on_delete=models.DO_NOTHING,default=None,null=True)
    city = models.ForeignKey(City,on_delete=models.DO_NOTHING,default=None,null=True)
    tax_identification_no = models.CharField(max_length=255, null=True,default='')
    email = models.CharField(max_length=255, default='',null=True)
    contact_no = models.CharField(max_length=255, default='',null=True)
    physical_address = models.CharField(max_length=255,default='',null=True)
    postal_address = models.CharField(max_length=255, default='',null=True)
    parent_company = models.ForeignKey("self", on_delete=models.DO_NOTHING, default=None,null=True, related_name="prnt_company")
    reporting_currency = models.ForeignKey(Currency,on_delete=models.DO_NOTHING, default=None,null=True)
    is_group_company = models.IntegerField( null=True,default=0)
    company_logo = models.CharField(max_length=255, null=True,default='')
    default_theme_color = models.CharField(max_length=255, null=True,default='')
    default_theme_text_color = models.CharField(max_length=255, null=True,default='')
    default_secondary_color = models.CharField(max_length=255, null=True,default='')
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'company'
