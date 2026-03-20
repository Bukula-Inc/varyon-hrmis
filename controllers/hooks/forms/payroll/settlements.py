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

def on_arrears_save (dbms, object):
    emp = DataConversion.safe_get (object.body, "employee")
    arrears = DataConversion.safe_get (object.body, "arrears", [])
    if not emp:
        throw (f"Employee No is <strong class='text-rose-600'>Required</strong>")
    if len (arrears) <= 0:
        throw (f"Recoverable's are <strong class='text-rose-600'>Required</strong>")
    
    for i, settlement_obj in enumerate (arrears):
        amount = DataConversion.safe_get (settlement_obj, "amount")
        rp = DataConversion.safe_get (settlement_obj, "repayment_period")
        if not amount:
            throw (f"Amount on ROW #{i+1} is <strong class='text-rose-600'>Required</strong>")
        if not rp:
            throw (f"Repayment Period on ROW #{i+1} is <strong class='text-rose-600'>Required</strong>")
        if not DataConversion.safe_get (settlement_obj, "salary_component"):
            throw (f"Salary Component on ROW #{i+1} is <strong class='text-rose-600'>Required</strong>")
        mrp = DataConversion.convert_to_float (amount) / DataConversion.convert_to_float (rp)
        DataConversion.safe_set (settlement_obj, "monthly_repayment", mrp)

    DataConversion.safe_set (object.body, "arrears", arrears)

def on_arrears_submit (dbms, object):
    core_payroll = Core_Payroll (dbms)
    emp = DataConversion.safe_get (object.body, "employee")
    arrears = DataConversion.safe_get (object.body, "arrears", [])
    if not emp:
        throw (f"Employee No is <strong class='text-rose-600'>Required</strong>")
    if len (arrears) <= 0:
        throw (f"Recoverable's are <strong class='text-rose-600'>Required</strong>")
    
    for i, settlement_obj in enumerate (arrears):
        amount = DataConversion.safe_get (settlement_obj, "amount")
        rp = DataConversion.safe_get (settlement_obj, "repayment_period")
        sc = DataConversion.safe_get (settlement_obj, "salary_component")
        if not amount:
            throw (f"Amount on ROW #{i+1} is <strong class='text-rose-600'>Required</strong>")
        if not rp:
            throw (f"Repayment Period on ROW #{i+1} is <strong class='text-rose-600'>Required</strong>")
        if not sc:
            throw (f"Salary Component on ROW #{i+1} is <strong class='text-rose-600'>Required</strong>")
        mrp = DataConversion.convert_to_float (amount) / DataConversion.convert_to_float (rp)

        DataConversion.safe_set (settlement_obj, "monthly_repayment", mrp)

        r = core_payroll.notify_payroll (emp, amount, sc, "Payroll_Recovery", DataConversion.safe_get (object.body, "name"), rp, entry_type="Earning")
    DataConversion.safe_set (object.body, "arrears", arrears)