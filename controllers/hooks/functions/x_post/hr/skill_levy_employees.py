from controllers.core_functions.hr import Core_Hr
from controllers.utils import Utils

utils = Utils()
throw = utils.throw
pp = utils.pretty_print

def company_skill_levy(dbms, object):
    get_employees = dbms.get_list("Employee", privilege=True, filters={"status": "Active"})
    employees = []
    if get_employees.status == utils.ok:
        emp_data = get_employees.data.rows
        for emp in emp_data:
            employees.append({
                "employee": emp['name'],
                "full_name": emp['full_name'],
                "designation": emp['designation'],
                "basic_pay": emp['basic_pay']
            })
    return utils.respond(utils.ok, {"data": employees})
            