from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr
from controllers.utils.data_conversions import DataConversion
from controllers.core_functions.payroll import Core_Payroll

utils = Utils ()
dates = Dates ()
pp = utils.pretty_print
throw = utils.throw

def on_gratuity_save(dbms, object):
    core_hr = Core_Hr(dbms)
    dt = DataConversion.safe_get(object, "body")
    contract = core_hr.get_doc("Hr_Contract", DataConversion.safe_get(dt, "contract"))

    previous_processed = DataConversion.convert_to_float(DataConversion.safe_get(contract, "previous_processed", 0))
    basic_salary = DataConversion.convert_to_float(DataConversion.safe_get(dt, "basic_salary", 0))
    by = 35 / 100
    
    eff_date = DataConversion.safe_get(dt, "effective_date") if not previous_processed else DataConversion.safe_get(dt, "last_pp_date")
    expiry_dt = DataConversion.safe_get(dt, "expiry_contract_date")
    
    if not expiry_dt:
        throw("Expiry Date is <b class='text-rose-600'>Required!</b>")

    wyd = DataConversion.date_diff(eff_date, expiry_dt, "months")
    wy_ttd = DataConversion.date_diff(eff_date, dates.today(), "months")
    
    if not contract:
        throw("Contract is <b class='text-rose-600'>Not Found!</b>")

    gratuity_pay = 0.00

    if wyd <= wy_ttd:
        gratuity_pay = basic_salary * wyd * by
    elif wyd / 2 >= wy_ttd:
        DataConversion.safe_set(object.body, "previous_processed", 1)
        DataConversion.safe_set(object.body, "last_pp_date", dates.today())
        gratuity_pay = basic_salary * wy_ttd * by

    if not gratuity_pay:
        throw("Gratuity Pay is <b class='text-rose-600'>Zero</b>")

    pp(gratuity_pay)

    # DataConversion.safe_set(object.body, "gratuity_amount", round(gratuity_pay, 2))  # Round to 2 decimal places

def on_gratuity_submit (dbms, object):    
    on_gratuity_save (dbms, object)
    core_hr = Core_Hr (dbms)
    cp = Core_Payroll (dbms)

    contract = core_hr.get_doc ("Hr_Contract", DataConversion.safe_get (object.body, "contract"))

    if not contract:
        throw ("Contract is <b class='text-rose-600'>Not Found!</b>")

    # DataConversion.safe_set (contract, "last_pp_date", DataConversion.safe_get (object.body, "last_pp_date"))
    # DataConversion.safe_set (contract, "previous_processed",  DataConversion.safe_get (object.body, "previous_processed"))

    r = cp.notify_payroll (
        DataConversion.safe_get(object.body, "employee"),
        DataConversion.convert_to_float (DataConversion.safe_get (object.body, "gratuity_amount")),
        entry_type="Earning",
        sc="Gratuity",
        doc_type="Gratuity",
        doc_name=DataConversion.safe_get (object.body, "name"),
    )

    pp (r)

    p_r = dbms.update ("Hr_Contract", contract, update_submitted=True)

    pp (r, p_r)