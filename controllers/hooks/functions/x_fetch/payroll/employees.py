from controllers.utils.data_conversions import DataConversion
from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr

utils = Utils ()
pp = utils.pretty_print
throw = utils.throw


def load_temp_employees (dbms, object):
    core_hr = Core_Hr (dbms)
    return_list = []
    employees = core_hr.get_list ("Employee", filters={"employment_type__in": ["Temporal", "Seasonal Employment"]})
    if employees:
        for employee in employees:
            DataConversion.safe_list_append (return_list, {
                "employee_no": DataConversion.safe_get (employee, "name"),
                "basic_pay": utils.decimal (DataConversion.convert_to_float(DataConversion.safe_get (employee, "basic_pay")), 2),
                "full_name": DataConversion.safe_get (employee, "full_name", f"""{DataConversion.safe_get (employee, 'first_name')} {DataConversion.safe_get (employee, 'middle_name', '')} {DataConversion.safe_get (employee, 'last_name')}""")
            })
        
    return utils.respond (utils.ok, return_list)