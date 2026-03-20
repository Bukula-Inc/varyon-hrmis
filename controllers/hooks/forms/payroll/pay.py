from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.payroll import Core_Payroll
from controllers.core_functions.hr import Core_Hr
from controllers.utils.data_conversions import DataConversion
from datetime import datetime


dates = Dates ()

utils = Utils ()
pp = utils.pretty_print
throw = utils.throw

def on_serve_seasonal_and_temp_pay (dbms, object):
    obj = DataConversion.safe_get (object, "body")
    DataConversion.safe_set (object.body, "is_current", 0)
    for i, em in enumerate (DataConversion.safe_get (obj, "employee", [])):
        basic = DataConversion.convert_to_float (DataConversion.safe_get (em, "basic_pay", 0))
        rate = DataConversion.convert_to_float (DataConversion.safe_get (em, "rate", 0))
        days = DataConversion.convert_to_float (DataConversion.safe_get (em, "days", 0))
        pay = DataConversion.convert_to_float (DataConversion.safe_get (em, "pay", 0))
        if not basic:
            throw (f"Basic Pay For Employee in <strong class='text-rose-600'>Row #{i+1} is messing</strong>")
        if not days:
            throw (f"Days Worked For Employee in <strong class='text-rose-600'>Row #{i+1} is messing</strong>")
        if not rate:
            rate = basic / 26
        DataConversion.safe_set (em, "pay", rate * days)

def on_serve_seasonal_and_temp_pay_submit (dbms, object):
    core_hr = Core_Hr (dbms)
    on_serve_seasonal_and_temp_pay (dbms, object)
    curr_pays = core_hr.get_list ("Pay_For_Temps_Or_Seasonal_Employee", {"is_current": 1})
    if curr_pays:
        for curr_pay in curr_pays:
            DataConversion.safe_set (curr_pay, "is_current", 0)
            r = dbms.update ("Pay_For_Temps_Or_Seasonal_Employee", curr_pay, update_submitted=True)
            pp (r)
    DataConversion.safe_set (object.body, "is_current", 1)
    
    