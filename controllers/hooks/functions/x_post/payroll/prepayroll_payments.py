from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.data_conversions import DataConversion

utils =Utils()
dates =Dates()
pp =utils.pretty_print
throw =utils.throw

def create_pre_payment_doc(dbms, object):
    return_response =utils.from_dict_to_object({
        "status": utils.ok,
        "data": utils.from_dict_to_object({"emp": "", "pre_payroll_name":""}),
    })

    separation =DataConversion.safe_get(DataConversion.safe_get(DataConversion.safe_get(object, "body", {}), "data", {}), "separations", [])

    pre_payroll =utils.from_dict_to_object({
        "name": None,
        "total_amount": 0.00,
        "total_basic": 0.00,
        "total_gross": 0.00,
        "total_deduction": 0.00,
        "total_net": 0.00,
        "separations": separation
    })

    sep =""

    # for emp in separation:
    #     sep +=f"""{emp.employee}_"""
    # return_response.data.emp =sep
    # return_response.data.pre_payroll_name ="Pre-Payment-0001"
    # return utils.respond(return_response.status, return_response.data)
    try:
        create_pre_payment_doc =dbms.create("Pre_Payroll_payment", pre_payroll, submit_after_create=True)
        if create_pre_payment_doc.status ==utils.ok:
            DataConversion.safe_set (return_response, "status", DataConversion.safe_get (create_pre_payment_doc, "status"))
            for emp in separation:
                sep += f"""{DataConversion.safe_get (emp, 'employee')}_"""
            DataConversion.safe_set (return_response.data, "emp", sep)
            DataConversion.safe_set (return_response.data, "pre_payroll_name", f"{DataConversion.safe_get (create_pre_payment_doc.data, "name")}")
        
        else:
            DataConversion.safe_set (return_response, "status", DataConversion.safe_get (create_pre_payment_doc, "status"))
            DataConversion.safe_set (return_response, "data", DataConversion.safe_get (create_pre_payment_doc, "error_message"))
    except Exception as e:
            DataConversion.safe_set (return_response, "status", utils.unprocessable_entity)
            DataConversion.safe_set (return_response, "data", f"{e}")

    return utils.respond(return_response.status, return_response.data)