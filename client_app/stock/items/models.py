from django.db import models
from client_app.models import BaseModel, TableModel
from client_app.core.company.models import Company
from client_app.core.country.models import Country

class Stock_Item (BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True)
    item_code = models.CharField(null=True, unique=True, default="")
    item_type = models.CharField (max_length=255, default='', blank=True, null=True)
    item_category = models.CharField (max_length=255, default='', blank=True, null=True)
    default_unit_of_measure = models.CharField (max_length=255, default='', blank=True, null=True)
    brand = models.CharField (max_length=255, default='', blank=True, null=True)
    unit_price = models.FloatField(default=0.00, null=True)
    cost_price = models.FloatField(default=0.00, null=True)
    barcode = models.CharField (max_length=255, default='', blank=True, null=True)
    barcode_image = models.TextField (default='', blank=True)
    qr_code = models.CharField (max_length=255, default='', blank=True, null=True)
    description = models.TextField(null=True)
    country_of_origin = models.ForeignKey( Country, on_delete=models.DO_NOTHING, default=None, null=True)
    reorder_point = models.IntegerField (default=0, null=True)
    minimum_tax_value = models.FloatField (default=0.00, null=True, blank=True)
    is_rrp = models.IntegerField (default=0, null=True, blank=True)
    rrp = models.FloatField (default=0.00, null=True, blank=True)
    quantity_unit = models.CharField (max_length=255, default='', blank=True, null=True)
    packaging_unit = models.CharField (max_length=255, default='', blank=True, null=True)
    item_classification = models.CharField (max_length=255, default='', blank=True, null=True)
    create_item_on_smart = models.IntegerField ( default=1, blank=True, null=True)
    product_img = models.TextField (default='', null=True)
    country_of_origin = models.CharField(max_length=255, default='', blank=True, null=True)
    is_bundle = models.IntegerField (default=0, null=0)
    is_smart_invoice_registered = models.IntegerField (default=0, null=True)
    qty_in_bundle = models.FloatField (default=0.00, null=True)
    bundle_item = models.ForeignKey ('self', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)

    class Meta:
        db_table = 'stock_item'