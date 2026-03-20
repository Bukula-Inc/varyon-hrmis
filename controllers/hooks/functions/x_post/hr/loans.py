from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.payroll import Core_Payroll
from controllers.utils.data_conversions import DataConversion


dates = Dates ()

utils = Utils ()
pp = utils.pretty_print
throw = utils.throw

def long_term_sponsorship_fund_request (dbms, object):
    core_payroll = Core_Payroll (dbms)
    status = utils.ok
    msg = "Done"
    req_fun = DataConversion.safe_get (object.body, "data")
    ref = DataConversion.safe_get (req_fun, "reference")
    if not DataConversion.safe_get (req_fun, "employee"):
        throw ("Employee No is <strong class='text-rose-600'>required</strong>.")
    
    if not ref:
        throw (f"Long Term Sponsorship Reference is <strong class='text-rose-600'>missing</strong>.")
    
    doc = core_payroll.get_doc ("Long_Term_Sponsorship", ref)
    
    if not doc:
        throw (f"Long Term Sponsorship with Reference {ref} was not <strong class='text-rose-600'>Found</strong>.")
    
    n_req = utils.from_dict_to_object (
        {
            "employee": DataConversion.safe_get (req_fun, "employee"),
            "reference": ref,
            "boarding_and_lodging": DataConversion.convert_to_float (DataConversion.safe_get (req_fun, "boarding_and_lodging", 0)),
            "travel_costs": DataConversion.convert_to_float (DataConversion.safe_get (req_fun, "travel_costs", 0)),
            "lunch_allowance": DataConversion.convert_to_float (DataConversion.safe_get (req_fun, "lunch_allowance", 0)),
            "books_allowance": DataConversion.convert_to_float (DataConversion.safe_get (req_fun, "books_allowance", 0)),
            "tuition_fees": DataConversion.convert_to_float (DataConversion.safe_get (req_fun, "tuition_fees", 0)),
            "others":  DataConversion.convert_to_float (DataConversion.safe_get (req_fun, "others", 0)),
        }
    )
    
    r = dbms.create ("Long_Term_Sponsorship_Fund_Request", n_req)
    pp (r)
    
    return utils.respond (status, msg)