from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr
from controllers.utils.data_conversions import DataConversion
from controllers.utils.dates import Dates

utils = Utils()
dates = Dates()

def employee_on_leave(dbms,object):
    core_hr = Core_Hr (dbms)
    filters = DataConversion.safe_get (object, "filters")
    DataConversion.safe_set (filters, "docstatus", 1)
    DataConversion.safe_set (filters, "status__in", ["Approved"])
    
    employee_leave = core_hr.get_list("Leave_Application", filters=filters)

    if DataConversion.safe_e (DataConversion.safe_get (employee_leave, "status"),'Approved', str, True) and DataConversion.safe_e (DataConversion.safe_get (employee_leave, "status"), utils.no_content, int,):
        return employee_leave

    
    utils.throw(employee_leave)