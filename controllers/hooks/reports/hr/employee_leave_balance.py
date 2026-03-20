from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr
from controllers.utils.data_conversions import DataConversion

utils = Utils()
dates = Dates()
pp =utils.pretty_print

def employee_leave_balance(dbms, object):
    core_hr = Core_Hr (dbms)
    leave_entry_data_result =[]
    filters = DataConversion.safe_get (object, "filters")
    DataConversion.safe_set (filters, "docstatus", 1)
    DataConversion.safe_set (filters, "is_active", 1)
    DataConversion.safe_set (filters, "status__in", ["Submitted"])
    leave_entry_list = core_hr.get_list("Leave_Entry", filters={"docstatus": 1, "status__in": ["Submitted"], "is_active": 1})

    employee_dict = {DataConversion.safe_get (emp, 'name'): emp for emp in core_hr.get_list("Employee")}
    
    for leave_entry in leave_entry_list:
        if not isinstance(leave_entry, dict):
            continue

        employee = DataConversion.safe_get (employee_dict, DataConversion.safe_get (leave_entry, "employee"))

        if employee:
            department = DataConversion.safe_get (employee, 'department')
            leave_entry_row = {}
            
            DataConversion.safe_set (leave_entry_row, "name", DataConversion.safe_get (leave_entry, "name", ""))
            DataConversion.safe_set (leave_entry_row, "leave_type", DataConversion.safe_get (leave_entry, "leave_type", ""))
            DataConversion.safe_set (leave_entry_row, "employee", DataConversion.safe_get (leave_entry, "employee", ""))
            DataConversion.safe_set (leave_entry_row, "employee_name", DataConversion.safe_get (leave_entry, "employee_name", ""))
            DataConversion.safe_set (leave_entry_row, "department", department)
            DataConversion.safe_set (leave_entry_row, "remaining_leave", DataConversion.safe_get (leave_entry, "employee_name", ""))
            DataConversion.safe_set (leave_entry_row, "used_leave", DataConversion.safe_get (leave_entry, "remaining_leave_days", 0))

            leave_entry_data_result.append(leave_entry_row)

    return utils.respond(utils.ok, {'rows': leave_entry_data_result})
