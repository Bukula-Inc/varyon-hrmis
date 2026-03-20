
from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.data_conversions import DataConversion
from controllers.core_functions.hr import Core_Hr


utils = Utils()
dates = Dates()

throw = utils.throw
pp = utils.pretty_print
from collections import defaultdict

def employee_grievance_report(dbms, object):
    core_hr = Core_Hr (dbms)

    grievances = []
    grievances_raised = defaultdict(int) 
    grievances_received = defaultdict(int)  
    filters = DataConversion.safe_get (object, "filters", {})
    DataConversion.safe_set (filters, "docstatus", 1)

    grievance_data = core_hr.get_list("Employee_Grievance", filters=filters, fetch_linked_fields=True)
    if grievance_data:
        for grievance in grievance_data:
            griever = DataConversion.safe_get (grievance, "employee_name")  
            grieved = DataConversion.safe_get (grievance, "grievance_against")  
            
            grievances_raised[griever] += 1
            grievances_received[grieved] += 1

        for grievance in grievance_data:
            grievance_dict = utils.from_dict_to_object({})
            DataConversion.safe_set (grievances, grievance_dict, grievance)

    return utils.respond(utils.ok, {"rows": grievances})