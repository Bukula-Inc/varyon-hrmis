from controllers.utils import Utils
from controllers.utils.data_conversions import DataConversion
from controllers.core_functions.hr import Core_Hr

utils = Utils ()
pp = utils.pretty_print
throw = utils.throw

def link_component_to_all_employees (dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    success = []
    failed = []
    component = DataConversion.safe_get (object.body, "data")
    employees = core_hr.get_list ("Employee", filters={"status__in": ["Active", "Suspended", "On Leave"]}, fetch_linked_tables=True)
    total = len (employees)
    if not component:
        throw ("Please Select <strong class='text-red-600'>Component Before Proceeding</strong>")
    if not employees:
        throw ("No <strong class='text-red-600'>Employee Found</strong>")

    for employee in employees:
        try:
            updated_bool = False
            component_type = DataConversion.safe_get (component, "component_type")
            comp = DataConversion.safe_get (component, "name")
            deductions = DataConversion.safe_get (employee, "deductions", [])
            earnings = DataConversion.safe_get (employee, "earnings", [])

            if component_type == "Earning":
                if earnings:
                    earning_dict = utils.array_to_dict (earnings, "earning")
                    if comp not in earning_dict:
                        DataConversion.safe_list_append (earnings, {"earning": comp})
                        updated_bool = True
                    else:
                        DataConversion.safe_list_append (failed, {"EMP-NO": DataConversion.safe_get (employee, "name"), "error_message": "Already Has The Component"})
                else:
                    earnings = []
                    DataConversion.safe_list_append (earnings, {"earning": comp})
                    updated_bool = True
                DataConversion.safe_set (employee, "earnings", earnings)

            elif component_type == "Deduction":
                if deductions:
                    deduction_dict = utils.array_to_dict (deductions, "deduction")
                    if comp not in  deduction_dict:
                        DataConversion.safe_list_append (deductions, {"deduction": comp})
                        updated_bool = True
                    else:
                        DataConversion.safe_list_append (failed, {"EMP-NO": DataConversion.safe_get (employee, "name"), "error_message": "Already Has The Component"})
                else:
                    deductions = []
                    DataConversion.safe_list_append (deductions, {"deduction": comp})
                    updated_bool = True
                DataConversion.safe_set (employee, "deductions", deductions)
            if updated_bool:
                r = dbms.update ("Employee", employee, update_submitted=True)

                if r.status == utils.ok:
                    DataConversion.safe_list_append (success, {"EMP-NO": DataConversion.safe_get (employee, "name"), "success_message": "Successfully "})
                else:
                    DataConversion.safe_list_append (failed, {"EMP-NO": DataConversion.safe_get (employee, "name"), "error_message": f"{DataConversion.safe_get (r.error_massage)}"})
        except Exception as err:
            pp (f"Error: {err}")
            DataConversion.safe_list_append (failed, {"EMP-NO": DataConversion.safe_get (employee, "name"), "error_message": f"{err}"})
            pass
    return utils.respond (utils.ok, response=f"Success: {len (success)} And Failed: {len (failed)} of Total: {total}")