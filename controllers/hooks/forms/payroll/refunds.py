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

def on_refund_save (dbms, object):
    emp = DataConversion.safe_get (object.body, "employee")
    refunds = DataConversion.safe_get (object.body, "refunds", [])
    if not emp:
        throw (f"Employee No is <strong class='text-rose-600'>Required</strong>")
    if len (refunds) <= 0:
        throw (f"Refunds are <strong class='text-rose-600'>Required</strong>")
    
    for i, refundable in enumerate (refunds):
        amount = DataConversion.safe_get (refundable, "amount")
        if not amount:
            throw (f"Amount on ROW #{i+1} is <strong class='text-rose-600'>Required</strong>")
        if not DataConversion.safe_get (refundable, "salary_component"):
            throw (f"Salary Component on ROW #{i+1} is <strong class='text-rose-600'>Required</strong>")

    DataConversion.safe_set (object.body, "refunds", refunds)

def on_refund_submit (dbms, object):
    core_payroll = Core_Payroll (dbms)
    emp = DataConversion.safe_get (object.body, "employee")
    refunds = DataConversion.safe_get (object.body, "refunds", [])
    if not emp:
        throw (f"Employee No is <strong class='text-rose-600'>Required</strong>")
    if len (refunds) <= 0:
        throw (f"Refunds are <strong class='text-rose-600'>Required</strong>")
    
    for i, refundable in enumerate (refunds):
        amount = DataConversion.safe_get (refundable, "amount")
        sc = DataConversion.safe_get (refundable, "salary_component")
        if not amount:
            throw (f"Amount on ROW #{i+1} is <strong class='text-rose-600'>Required</strong>")
        if not sc:
            throw (f"Salary Component on ROW #{i+1} is <strong class='text-rose-600'>Required</strong>")

        r = core_payroll.notify_payroll (emp, amount, sc, "Payroll_Refund", DataConversion.safe_get (object.body, "name"), entry_type="Earning")
        pp (r)

    DataConversion.safe_set (object.body, "refunds", refunds)