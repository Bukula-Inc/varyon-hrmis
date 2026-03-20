from controllers.core_functions.hr import Core_Hr
from controllers.utils import Utils
from controllers.utils.data_conversions import DataConversion

utils = Utils ()
pp = utils.pretty_print
throw = utils.throw

def on_salary_component_save (dbms, object):
    if DataConversion.safe_get (object.body, "is_grossable"):
        DataConversion.safe_set (object.body, "is_grossable", 1)
    DataConversion.safe_set (object.body, "exclude_on_statutory_deductions", DataConversion.safe_get (object.body, "exclude_on_statutory_deductions", 0))
    if DataConversion.safe_e (object.body.value_type, "custom", str, to_lower=True):
        DataConversion.safe_set (object.body, "fixed_amount", 0)
        DataConversion.safe_set (object.body, "percentage", 0)
    elif DataConversion.safe_e (object.body.value_type, "percentage", str, to_lower=True):
        DataConversion.safe_set (object.body, "fixed_amount", 0)
    elif  DataConversion.safe_e (object.body.value_type, "fixed amount", str, to_lower=True):
        DataConversion.safe_set (object.body, "percentage", 0)
    if DataConversion.safe_get (object.body, "unstandardized", 0):
        if DataConversion.safe_e (object.body.value_type, "custom", str, to_lower=True):
            throw ("When You unstandardized a salary Component Value Type cannot be <strong class='text-rose-600'>Custom</strong> ")
    DataConversion.safe_set (object.body, "old_name", DataConversion.safe_get (object.body, "name"))

def on_salary_component_update(dbms, object):
    core_hr = Core_Hr (dbms)
    DataConversion.safe_set (object.body, "exclude_on_statutory_deductions", DataConversion.safe_get (object.body, "exclude_on_statutory_deductions", 0))
    if DataConversion.safe_e (object.body.value_type, "custom", str, to_lower=True):
        DataConversion.safe_set (object.body, "fixed_amount", 0)
        DataConversion.safe_set (object.body, "percentage", 0)
    elif DataConversion.safe_e (object.body.value_type, "percentage", str, to_lower=True):
        DataConversion.safe_set (object.body, "fixed_amount", 0)
    elif  DataConversion.safe_e (object.body.value_type, "fixed amount", str, to_lower=True):
        DataConversion.safe_set (object.body, "percentage", 0)
    if DataConversion.safe_get (object.body, "unstandardized", 0):
        if DataConversion.safe_e (object.body.value_type, "custom", str, to_lower=True):
            throw ("When You unstandardized a salary Component Value Type cannot be <strong class='text-rose-600'>Custom</strong> ")


