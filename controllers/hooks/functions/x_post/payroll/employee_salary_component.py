from controllers.utils import Utils
from controllers.utils.data_conversions import DataConversion
from controllers.core_functions.hr import Core_Hr
utils = Utils ()
pp =utils.pretty_print
throw = utils.throw

def allocate_employee_salary_component(dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    data = object.body.data
    success = []
    failed = []
    if data:
        component = DataConversion.safe_get (data, "name")
        component_type = str (DataConversion.safe_get (data, "component_type")).lower ()
        employees = DataConversion.safe_get (data, "employee", [])
        total = len (employees)
        
        if not component:
            throw ("Please Select <strong class='text-red-600'>Component Before Proceeding</strong>")
        if not component_type:
            throw ("Please Select <strong class='text-red-600'>Component Before Proceeding</strong>")
        if not employees or len(employees) <= 0:
            throw ("No <strong class='text-red-600'>Employee Found</strong>")

        for emp in employees:
            try:
                update_bool = False
                lis_ = []
                employee_data = core_hr.get_doc ("Employee", DataConversion.safe_get(emp, "employee"))
                if employee_data:
                    if component_type == "earning":
                        lis_ = DataConversion.safe_get (employee_data, "earnings", [])
                        earnings = utils.array_to_dict (lis_, "earning")
                        if earnings:
                            if component not in earnings:
                                DataConversion.safe_list_append (lis_, {"earning": component})
                                update_bool = True
                            else:
                                DataConversion.safe_list_append (failed, {"EMP-NO": DataConversion.safe_get (emp, "name"), "error_message": "Already Has The Component"})
                        else:
                            DataConversion.safe_list_append (lis_, {"earning": component})
                            update_bool = True
                        DataConversion.safe_set (employee_data, "earnings", lis_)
                    elif component_type == "deduction":
                        lis_ = DataConversion.safe_get (employee_data, "deductions", [])
                        deductions = utils.array_to_dict (lis_, 'deduction')
                        if deductions:
                            if component not in deductions:
                                DataConversion.safe_list_append (lis_, {"deduction": component})
                                update_bool = True
                            else:
                                DataConversion.safe_list_append (failed, {"EMP-NO": DataConversion.safe_get (emp, "name"), "error_message": "Already Has The Component"})
                        else:
                            DataConversion.safe_list_append (lis_, {"deduction": component})
                            update_bool = True
                        DataConversion.safe_set (employee_data, "deductions", lis_)
                if update_bool:
                    updated =  dbms.update ("Employee", employee_data,  update_submitted=True)
                    if updated.status == utils.ok:
                        DataConversion.safe_list_append (success, {"EMP-NO": DataConversion.safe_get (emp, "name"), "success_message": "Successfully "})
                    else:
                        DataConversion.safe_list_append (failed, {"EMP-NO": DataConversion.safe_get (emp, "name"), "error_message": f"{DataConversion.safe_get (updated.error_massage)}"})
            except Exception as err:
                pp (f"ERROR {err}", DataConversion.safe_get (employee_data, "name"))
                pass
    return utils.respond (status=utils.ok, response=f"Success: {len (success)} And Failed: {len (failed)} of Total: {total}")