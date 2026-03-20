from controllers.utils import Utils
from controllers.utils.data_conversions import DataConversion
from controllers.core_functions.hr import Core_Hr
from controllers.utils.dates import Dates

utils = Utils()
dates = Dates()

throw = utils.throw
pp = utils.pretty_print



def employee_exit_report(dbms,object):
    core_hr = Core_Hr (dbms)
    exiting_employees = []
    filters = DataConversion.safe_get (object, "filters")
    DataConversion.safe_set (filters, "docstatus", 1)

    exited_emp = core_hr.get_list("Employee_Seperation", filters={"docstatus":1}, fetch_linked_fields=True)
    if exited_emp:
        for emp_data in exited_emp:
            emp = DataConversion.safe_get (emp_data.linked_fields, "employee")
            emp_dict = utils.from_dict_to_object()
            DataConversion.safe_get (emp_dict, "employee", DataConversion.safe_get (emp, "name"))
            DataConversion.safe_get (emp_dict, "employee_name", DataConversion.safe_get (emp, "full_name"))
            DataConversion.safe_get (emp_dict, "date_of_joining", DataConversion.safe_get (emp, "date_of_joining"))
            DataConversion.safe_get (emp_dict, "resignation_date", DataConversion.safe_get (emp_data, "resignation_date"))
            DataConversion.safe_get (emp_dict, "interview_summary", "")
            DataConversion.safe_get (emp_dict, "department", DataConversion.safe_get (emp, "department"))
            DataConversion.safe_get (emp_dict, "Designation", DataConversion.safe_get (emp, "designation"))
            DataConversion.safe_get (emp_dict, "reports_to", DataConversion.safe_get (emp, "report_to"))
            DataConversion.safe_list_append (exiting_employees, emp_dict)

    return utils.respond(utils.ok, {"rows": exiting_employees})