from controllers.utils import Utils
from controllers.utils.dates import Dates 
from controllers.core_functions.payroll import Core_Payroll
from controllers.utils.data_conversions import DataConversion

utils = Utils()
dates = Dates ()
pp = utils.pretty_print
throw = utils.throw

def transfer_file_report(dbms, object):
    core_payroll = Core_Payroll (dbms=dbms)
    filters = {}
    transfer_file_data_result = []
    filter_obj = DataConversion.safe_get (object, "filters", utils.from_dict_to_object ())
    emps =  utils.array_to_dict (core_payroll.fetch_data_from_sql ("SELECT name, full_name, bank_name, account_no, sort_code, first_name, middle_name, last_name FROM employee"), "name")

    order_by = ['-id']
    from_date = DataConversion.safe_get (filter_obj, "from_date", None)
    to_date = DataConversion.safe_get (filter_obj, "to_date", None)

    totals = utils.from_dict_to_object ({
        "employee": " OVERALL TOTAL",
        "amount": 0,
        "is_opening_or_closing": True
    })

    if not from_date and not to_date:
        DataConversion.safe_list_append (transfer_file_data_result, totals)
        throw ("Please Select the <strong class='text-blue-600'>From and To Dates</strong>")
    
    from_date = DataConversion.safe_get (filter_obj, "from_date")
    to_date = DataConversion.safe_get (filter_obj, "to_date")

    DataConversion.safe_set (filters, "from_date__range", [from_date, to_date])
    exclude_these_emp = {}
    payroll_processors = core_payroll.get_list ("Payroll_Processor", filters=filters, order_by=order_by, limit=15)
    exclude_these = core_payroll.get_list ("With_Hold_Employee_Pay", filters=filters, order_by=order_by, limit=15)

    if exclude_these:
        excluded = []
        for exclude_list in exclude_these:
            excluded.extend (DataConversion.safe_get (exclude_list, "employees", []))
        exclude_these_emp = utils.array_to_dict (excluded, "employee")
    
    if payroll_processors and len (payroll_processors) > 0:
        track_emp = []
        for payroll_processor in payroll_processors:
            employees = DataConversion.safe_get (payroll_processor, "employee_info", [])
            if employees and len (employees) > 0:
                for emp in employees:
                    name = DataConversion.safe_get (emp, "employee", '')
                    if DataConversion.safe_get (exclude_these_emp, name):
                        continue
                    if name not in track_emp:
                        track_emp.append (name)
                        emp_ = DataConversion.safe_get (emps, name)
                        if emp_:
                            net = DataConversion.convert_to_float (DataConversion.safe_get (emp, "net", 0.00))
                            DataConversion.safe_list_append (transfer_file_data_result, {
                                "employee": name,
                                "employee_names": DataConversion.safe_get (emp, "full_names", ''),
                                "bank_name": DataConversion.safe_get (emp_, "bank_name", ''),
                                "bank_account_no": DataConversion.safe_get (emp_, "account_no", ''),
                                "sort_code": DataConversion.safe_get (emp_, "sort_code", ''),
                                "amount": net,
                                "description": f"""{DataConversion.safe_get (emp, "full_names", '')}'s Pay For {DataConversion.safe_get (payroll_processor, "to_date")}"""
                            })
                            totals.amount += net

    DataConversion.safe_list_append (transfer_file_data_result, totals)
    return utils.respond(utils.ok, {'rows': transfer_file_data_result})