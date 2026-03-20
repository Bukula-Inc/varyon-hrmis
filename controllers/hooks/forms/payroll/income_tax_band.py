from controllers.utils import Utils
from controllers.utils.data_conversions import DataConversion

utils = Utils()


def before_income_tax_band_save(dbms,object):
    body = DataConversion.safe_get (object, "body")
    DataConversion.safe_set (object.body, "zra_percentage", DataConversion.convert_to_float (DataConversion.safe_get (body, "zra_percentage", 37)))
    DataConversion.safe_set (object.body, "take_home_percentage", 100 - DataConversion.convert_to_float (DataConversion.safe_get (body, "zra_percentage", 37)))

    tax_band_data = dbms.get_list("Income_Tax_Band", filters={"is_current":1}, privilege=True)
    if tax_band_data.status == utils.ok:
        tax_band = tax_band_data.data.rows
        for band in tax_band:
            band.is_current = 0
            update = dbms.update("Income_Tax_Band", band, privilege=True)